from pydantic import BaseModel, Field

class GetCurrentWeatherInput(BaseModel):
    latitude: float = Field(ge=-90, le=90, description='Latitude of the location to fetch current weather data for')
    longitude: float = Field(ge=-90, le=90, description='Longitude of the location to fetch current weather data for')

class GetForecastWeatherInput(BaseModel):
    latitude: float = Field(ge=-90, le=90, description='Latitude of the location to fetch forecast weather data for')
    longitude: float = Field(ge=-90, le=90, description='Longitude of the location to fetch forecast weather data for')
    forecast_days: int = Field(default=7, ge=1, le=16, description='Number of days to forecast. Default is 7, maximum is 16.')