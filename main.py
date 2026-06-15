import os
import time
from functools import wraps

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='web', static_url_path='')
CORS(app)


PROXY_URL = ""  # YOUR_PROXY_HERE(Support HTTPS, HTTP, SOCS5 etc....)

if PROXY_URL:
    PROXIES = {"http": PROXY_URL, "https": PROXY_URL}
    print(f"🔒 Using Proxy: {PROXY_URL}")
else:
    PROXIES = None
    print("Proxy don't work, using your Internet....")

# Config Files
CACHE_TIMEOUT = 300                     
REQUEST_TIMEOUT = (3.05, 6.05)          # (connect timeout, read timeout)
MAX_RETRIES = 2
BACKOFF_FACTOR = 0.5

# website mirrors 
WEATHER_SOURCES = [
    "https://wttr.in/{place}?format=j1",
    "https://weather.wttr.in/{place}?format=j1",   
]


def get_session():

    session = requests.Session()
    if PROXIES:
        session.proxies.update(PROXIES)


    retry_strategy = Retry(
        total=MAX_RETRIES,
        connect=MAX_RETRIES,
        read=MAX_RETRIES,
        backoff_factor=BACKOFF_FACTOR,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(
        max_retries=retry_strategy,
        pool_connections=20,
        pool_maxsize=20
    )
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


_weather_session = get_session()


def get_weather_icon(code, description):

    code = str(code)
    desc_lower = description.lower()
    if code in ["113"] or "sunny" in desc_lower or "clear" in desc_lower:
        return "☀️"
    if code in ["116"] or "partly" in desc_lower:
        return "⛅"
    if code in ["119", "122"] or "cloudy" in desc_lower or "overcast" in desc_lower:
        return "☁️"
    if code in ["176", "179", "182", "185", "263", "266", "281", "284", "293", "296",
                "299", "302", "305", "308", "356", "359", "362", "365", "368", "371",
                "374", "377"] or "rain" in desc_lower:
        return "🌧️"
    if code in ["200"] or "drizzle" in desc_lower:
        return "🌦️"
    if code in ["386", "389"] or "thunder" in desc_lower:
        return "⛈️"
    if code in ["227", "230", "320", "323", "326", "329", "332", "335", "338", "350",
                "353", "392", "395"] or "snow" in desc_lower:
        return "❄️"
    if code in ["143", "248", "260"] or "mist" in desc_lower or "fog" in desc_lower:
        return "🌫️"
    return "🌡️"

def fetch_weather_from_source(place):

    last_error = None
    for url_template in WEATHER_SOURCES:
        url = url_template.format(place=place)
        try:
            response = _weather_session.get(url, timeout=REQUEST_TIMEOUT)
            if response.status_code == 200:
                return response.json()
            last_error = f"HTTP {response.status_code}"
        except Exception as e:
            last_error = str(e)
            continue
    raise Exception(f"All sources failed: {last_error}")

# cache 
cache = {}

def cache_response(timeout=CACHE_TIMEOUT):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = request.full_path
            if cache_key in cache:
                cached_data, timestamp = cache[cache_key]
                if time.time() - timestamp < timeout:
                    return jsonify(cached_data)

            result = f(*args, **kwargs)
            if isinstance(result, tuple):
                response_data = result[0]
                status_code = result[1] if len(result) > 1 else 200
            else:
                response_data = result
                status_code = 200

            if status_code == 200 and isinstance(response_data, dict):
                cache[cache_key] = (response_data, time.time())
            return result
        return decorated_function
    return decorator


@app.route('/')
def index():
    return send_from_directory('web', 'main.html')

@app.route('/api/weather')
@cache_response(300)
def get_weather():
    place = request.args.get('city') or request.args.get('place')
    if not place or place.strip() == "":
        return jsonify({
            "success": False,
            "error": "Please provide a city name. Example: /api/weather?city=London"
        }), 400

    try:
        data = fetch_weather_from_source(place)

        if "error" in data:
            return jsonify({
                "success": False,
                "error": f"City '{place}' not found"
            }), 404

        current = data.get("current_condition", [{}])[0]
        if not current:
            return jsonify({
                "success": False,
                "error": f"No weather data available for '{place}'"
            }), 404

        temp_c = current.get("temp_C", "N/A")
        humidity = current.get("humidity", "N/A")
        wind_speed = current.get("windspeedKmph", "N/A")
        weather_desc = current.get("weatherDesc", [{}])[0].get("value", "Unknown")
        feels_like = current.get("FeelsLikeC", "N/A")
        weather_code = current.get("weatherCode", "0")
        weather_icon = get_weather_icon(weather_code, weather_desc)

        forecast_data = []
        for day in data.get("weather", [])[:5]:
            day_hourly = day.get("hourly", [{}])[0]
            forecast_data.append({
                "date": day.get("date", ""),
                "max_temp": day.get("maxtempC", "N/A"),
                "min_temp": day.get("mintempC", "N/A"),
                "description": day_hourly.get("weatherDesc", [{}])[0].get("value", "Unknown"),
                "icon": get_weather_icon(day_hourly.get("weatherCode", "0"), "")
            })

        return jsonify({
            "success": True,
            "data": {
                "city": place.title(),
                "temperature": f"{temp_c}°C",
                "temp_value": int(temp_c) if temp_c != "N/A" else None,
                "humidity": f"{humidity}%",
                "humidity_value": int(humidity) if humidity != "N/A" else None,
                "wind": f"{wind_speed} km/h",
                "wind_value": int(wind_speed) if wind_speed != "N/A" else None,
                "description": weather_desc,
                "feels_like": f"{feels_like}°C",
                "feels_like_value": int(feels_like) if feels_like != "N/A" else None,
                "icon": weather_icon,
                "forecast": forecast_data,
                "unit": "metric"
            }
        })

    except Exception as e:
        app.logger.error(f"Weather fetch error: {e}")
        return jsonify({
            "success": False,
            "error": f"Unable to fetch weather for '{place}'. Check network or proxy settings."
        }), 503

@app.route('/api/health')
def health():
    return jsonify({
        "status": "healthy",
        "message": "Weather API is running (proxy & retries enabled)",
        "timestamp": time.time()
    })

@app.route('/api/weather/legacy')
def get_weather_legacy():
    place = request.args.get('city') or request.args.get('place')
    if not place or place.strip() == "":
        return jsonify({"error": "Please enter a city name"}), 400
    try:
        data = fetch_weather_from_source(place)
        current = data.get("current_condition", [{}])[0]
        temp_c = current.get("temp_C", "N/A")
        humidity = current.get("humidity", "N/A")
        wind_speed = current.get("windspeedKmph", "N/A")
        weather_desc = current.get("weatherDesc", [{}])[0].get("value", "Unknown")
        feels_like = current.get("FeelsLikeC", "N/A")
        weather_code = current.get("weatherCode", "0")
        weather_icon = get_weather_icon(weather_code, weather_desc)
        return jsonify({
            "success": True,
            "city": place.title(),
            "temperature": f"{temp_c}°C",
            "temp_value": int(temp_c),
            "humidity": f"{humidity}%",
            "wind": f"{wind_speed} km/h",
            "description": weather_desc,
            "feels_like": f"{feels_like}°C",
            "icon": weather_icon
        })
    except Exception:
        return jsonify({"error": f"City '{place}' not found or blocked"}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)