from flask_app import app
from flask import jsonify, request
import requests
import os


API_SECRET_KEY = os.environ.get("API_SECRET_KEY")

def get_weather_data(city):
    try:
        api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_SECRET_KEY}"
        response = requests.get(api_url)
        data = response.json()
        temperature = round(data["main"]["temp"] - 273.15)
        weather_description = data["weather"][0]["description"]
        icon_code = data["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
        city = data["name"]
        return {
            "city": city,
            "temperature": temperature,
            "description": weather_description,
            "icon_url": icon_url
        }
    except Exception as e:
        print(e)
        return None


@app.route('/weather/<string:city>', methods=['GET'])
def weather(city):
    data = get_weather_data(city)
    if data:
        return jsonify(data)
    else:
        return jsonify({"message": "Failed to fetch weather data"}), 400