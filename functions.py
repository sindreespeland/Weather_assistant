import requests
from langchain.tools import tool
from models import GetCurrentWeatherInput, GetForecastWeatherInput
from datetime import datetime, timedelta
import pytz
from collections import Counter

def get_weather_description(code):
    weather_descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }
    return weather_descriptions.get(code, "Unknown")

def extract_current_weather(api_response):
    hourly_data = api_response['hourly']
    time_data = hourly_data['time']
    temperature_data = hourly_data['temperature_2m']
    weather_code_data = hourly_data['weather_code']
    
    # Get the timezone from the API response
    timezone = pytz.timezone(api_response['timezone'])
    
    # Get the current time in the timezone of the location
    current_time = datetime.now(timezone)
    
    # Convert API times to timezone-aware datetime objects
    api_times = [datetime.fromisoformat(t).replace(tzinfo=pytz.UTC).astimezone(timezone) for t in time_data]
    
    # Find the index of the closest time
    time_differences = [abs(current_time - t) for t in api_times]
    closest_index = time_differences.index(min(time_differences))
    
    current_temp = temperature_data[closest_index]
    current_weather_code = weather_code_data[closest_index]
    
    
    weather_description = get_weather_description(current_weather_code)
    
    return {
        "temperature": current_temp,
        "weather_description": weather_description,
        "time": api_times[closest_index].isoformat()
    }

def extract_forecast_weather(api_response, forecast_days):
    hourly_data = api_response['hourly']
    
    # Calculate the index for the day we want
    target_day_start = 24 * (forecast_days - 1)
    target_day_end = target_day_start + 24
    
    target_date = (datetime.now() + timedelta(days=forecast_days - 1)).strftime('%Y-%m-%d')
    
    temperatures = hourly_data['temperature_2m'][target_day_start:target_day_end]
    weather_codes = hourly_data['weather_code'][target_day_start:target_day_end]
    
    avg_temp = sum(temperatures) / len(temperatures)
    max_temp = max(temperatures)
    min_temp = min(temperatures)
    
    # Get the most common weather code for the day
    most_common_weather = Counter(weather_codes).most_common(1)[0][0]
    weather_description = get_weather_description(most_common_weather)
    
    return {
        "date": target_date,
        "average_temperature": round(avg_temp, 1),
        "max_temperature": round(max_temp, 1),
        "min_temperature": round(min_temp, 1),
        "weather_condition": weather_description,
    }



@tool(args_schema=GetCurrentWeatherInput)
def get_current_weather(latitude: float, longitude: float) -> dict:
    """Fetch the current weather and temperature for given coordinates"""

    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': ['temperature_2m', 'weather_code'],
        'forecast_days': 1
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        result = response.json()
        return extract_current_weather(result)
    else:
        raise Exception(f"API Request failed with status code: {response.status_code}")
    

@tool(args_schema=GetForecastWeatherInput)
def get_forecast_weather(latitude: float, longitude: float, forecast_days: int) -> dict:
    """Fetch forcast weather and temperature for a spescific day and for given coordinates"""

    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': ['temperature_2m', 'weather_code'],
        'forecast_days': forecast_days
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        result = response.json()
        return extract_forecast_weather(result, forecast_days)
    else:
        raise Exception(f"API Request failed with status code: {response.status_code}")
    