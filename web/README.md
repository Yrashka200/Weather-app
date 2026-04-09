# 🌤️ Weather App

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A beautiful desktop weather application built with Python and Eel framework, featuring a modern glass-morphism UI. Get real-time weather information for any city worldwide with dynamic weather icons and smooth animations.

![Weather App Screenshot](https://via.placeholder.com/800x400/87CEEB/FFFFFF?text=Weather+App+Screenshot)

##  Features

- **Real-time Weather Data**: Get current temperature, humidity, wind speed, and weather conditions
- **Dynamic Weather Icons**: Smart emoji-based icons that change with weather conditions (☀️ 🌧️ ❄️ ⛅)
- **Glass-morphism Design**: Modern UI with gradient backgrounds and smooth animations
- **Temperature Color Coding**: Visual indicators - blue for cold (<0°C), orange for hot (>30°C)
- **Responsive Layout**: Adapts to different screen sizes
- **Keyboard Support**: Press Enter to search for cities
- **Error Handling**: User-friendly messages for invalid inputs or network issues
- **Offline Ready**: Graceful handling of network connectivity issues

##  Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/Yrashka200/weather-app.git
   cd weather-app
   ```

2. **Install dependencies**
   ```bash
   pip install eel requests
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

The app will open in a new window with a beautiful weather interface!

##  Usage

1. Launch the application using `python main.py`
2. Enter a city name in the search box
3. Press Enter or click the search button
4. View real-time weather information with dynamic icons and colors
5. The background adapts based on temperature ranges

### Keyboard Shortcuts
- `Enter`: Search for weather data
- `Ctrl+C`: Exit the application (in terminal)

##  Project Structure

```
weather-app/
├── main.py              # Python backend with Eel bindings
├── web/
│   ├── main.html        # Main UI structure and JavaScript
│   ├── style.css        # Glass-morphism styling and animations
│   └── README.md        # Web interface documentation
└── README.md            # Project documentation (this file)
```

##  Technologies Used

- **Python**: Backend logic and API integration
- **Eel**: Framework for building desktop apps with web technologies
- **HTML5/CSS3**: Modern web interface
- **JavaScript**: Dynamic UI interactions
- **OpenWeatherMap API**: Weather data source

##  Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
