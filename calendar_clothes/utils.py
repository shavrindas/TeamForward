# utils.py

import requests

def get_weather():
    api_key = 'your_openweathermap_api_key'  # 본인의 OpenWeatherMap API 키 입력
    lat = '37.5665'  # 서울의 위도
    lon = '126.978'  # 서울의 경도
    api_url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=kr'

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        weather_data = response.json()
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        weather = {
            'temperature': temperature,
            'description': description,
            'icon': icon
        }
        return weather
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather: {e}")
        return None
