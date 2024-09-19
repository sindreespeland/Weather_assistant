# Weather_assistant
Using langchain functions, tools and agents to create a weather assistant

## Project description

### Overview
The weather assistant provides users with weather information, temperature and forcast predictions.

### Objectives
**Step 1:**
1. Implement a basic conversational interface for weather queries
2. Integrate with a weather API to fetch data
3. Demonstrate the use of LangChain's functions, tools, and agents

**Step 2:**
4. Create a FE (react) and BE (fast api) which is powered by this chatbot
5. Display function outputs as widgets

**Step 3:**
6. Futuristic chat mode. Where you can talk to the chatbot. It only shows widgets and talks back the text.


## Step 1
### 1.1 Create functions and args schemas
**Get current weather and temperature:**

This function returns the current weather and temperature for given location.

Function inputs:
- latitude, longitude

Request params:
- latitude
- longitude
- hourly: temperature_2m (for temp), weather_code (needs to be interpreted for code to text)
- forecast_days: 1 (only need current day)

Output:
- current temp
- current weather
- time

**Get forecast weather and temperature**

This function returns the forcast weather and temperature for a given location

Function inputs:
- latitude, longitude
- forecast_days (7 is default, up to 16 days is possible)

Output:
- date
- avg temp for that day
- max and min temp
- weather

### 1.2 Initialize runnables for chain
**Converting functions to openai function descriptions:**
```python
functions = [convert_to_openai_function(f) for f in tools]
```
We use the convert_to_openai_function function to convert the functions into readable descriptions for the openai model. Openai expects a certain format for their functions.

**Instantiating the model:**
```python
model = ChatOpenAI(
    model='gpt-4o-mini',
    temperature=0
).bind(functions=functions)
```

**Creating a ChatPromptTemplate:**
```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are helpful weather assistant assistant. You will only answer weather related questions"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])
```
A ChatpromptTemplate is a structured way to create prompts for langage models. It allows you to define a template for how conversations should be formatted and what elements they should include.

It creates a structure that correctly formats the system messagem, previous history and current user input.