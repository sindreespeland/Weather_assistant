# Weather_assistant
Using langchain functions, tools and agents to create a weather assistant

## Project description

### Overview
The weather assistant provides users with weather information, temperature and forcast predictions.

### Objectives
1. Implement a basic conversational interface for weather queries
2. Integrate with a weather API to fetch data
3. Demonstrate the use of LangChain's functions, tools, and agents

### Functions
**Get current weather and temperature:**

This function returns the current weather and temperature for given location.

Function inputs:
- latitude, longitude

Request params:
- latitude
- longitude
- hourly: temperature_2m (for temp), weather_code (needs to be interpreted for code to text)
- forecast_days: 1 (only need current day)

**Get forecast weather and temperature**

This function returns the forcast weather and temperature for a given location

Function inputs:
- latitude, longitude
- forecast_days (7 is default, up to 16 days is possible)

