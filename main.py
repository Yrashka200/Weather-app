import eel
import requests
import json

@eel.expose
def get_weather(place):
    if not place or place.strip() == "":
        return json.dumps({"error": "Please enter a city name"})
    
    try:
        # Get full weather data from wttr.in
        url = f"https://wttr.in/{place}?format=j1"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        current = data.get("current_condition", [{}])[0]
        
        # Extract weather data
        temp_c = current.get("temp_C", "N/A")
        humidity = current.get("humidity", "N/A")
        wind_speed = current.get("windspeedKmph", "N/A")
        weather_desc = current.get("weatherDesc", [{}])[0].get("value", "Unknown")
        feels_like = current.get("FeelsLikeC", "N/A")
        weather_code = current.get("weatherCode", "0")
        
        # Map weather codes to icons
        weather_icon = get_weather_icon(weather_code, weather_desc)
        
        return json.dumps({
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
        
    except requests.RequestException as e:
        return json.dumps({"error": f"Network error. Please check your connection."})
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        return json.dumps({"error": f"City '{place}' not found. Please check the name."})

def get_weather_icon(code, description):
    """Return emoji/icon based on weather condition"""
    code = str(code)
    desc_lower = description.lower()
    
    # Sunny / Clear
    if code in ["113"] or "sunny" in desc_lower or "clear" in desc_lower:
        return "☀️"
    # Partly cloudy
    elif code in ["116"] or "partly" in desc_lower:
        return "⛅"
    # Cloudy / Overcast
    elif code in ["119", "122"] or "cloudy" in desc_lower or "overcast" in desc_lower:
        return "☁️"
    # Rain
    elif code in ["176", "179", "182", "185", "263", "266", "281", "284", "293", "296", "299", "302", "305", "308", "356", "359", "362", "365", "368", "371", "374", "377"] or "rain" in desc_lower:
        return "🌧️"
    # Drizzle
    elif code in ["200"] or "drizzle" in desc_lower:
        return "🌦️"
    # Thunderstorm
    elif code in ["386", "389"] or "thunder" in desc_lower:
        return "⛈️"
    # Snow
    elif code in ["227", "230", "320", "323", "326", "329", "332", "335", "338", "350", "353", "392", "395"] or "snow" in desc_lower:
        return "❄️"
    # Mist / Fog
    elif code in ["143", "248", "260"] or "mist" in desc_lower or "fog" in desc_lower:
        return "🌫️"
    else:
        return "🌡️"

eel.init('web')
eel.start('main.html', size=(900, 650))