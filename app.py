import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Replace 'YOUR_API_KEY' with your actual API key from OpenWeatherMap
api_key = 'db5dbc8cf25affca2c9f131fce71faad'

def get_weather_data(city_name):
    base_url = 'http://api.openweathermap.org/data/2.5/forecast'
    params = {'q': city_name, 'appid': api_key, 'units': 'metric'}  # 'units': 'metric' for Celsius

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        return weather_data
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city_name = request.form['city']
        weather_data = get_weather_data(city_name)

        if weather_data:
            temperature = weather_data['list'][0]['main']['temp']  # Get current temperature
            description = weather_data['list'][0]['weather'][0]['description']  # Get current weather description
            humidity = weather_data['list'][0]['main']['humidity']  # Get current humidity

            # Loop through hourly forecasts to find rainfall data
            rainfall = 0  # Initialize rainfall to 0
            for forecast in weather_data['list']:
                if 'rain' in forecast and '3h' in forecast['rain']:
                    rainfall += forecast['rain']['3h']

            return render_template('weather.html', city=city_name, temperature=temperature, description=description, humidity=humidity, rainfall=rainfall)
        else:
            error_message = f"Weather data not available for {city_name}."
            return render_template('weather.html', error=error_message)

    return render_template('weather.html')

if __name__ == '__main__':
    app.run(debug=True)
