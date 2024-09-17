from functions import get_current_weather, get_forecast_weather
from langchain_openai import ChatOpenAI
from langchain_core.utils.function_calling import convert_to_openai_function

result = get_forecast_weather.invoke({"latitude": 59.3293, "longitude": 18.0686, "forecast_days": 10})
print(result)

# make functions return only necessary data