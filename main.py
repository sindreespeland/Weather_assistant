from functions import get_current_weather, get_forecast_weather
from langchain_openai import ChatOpenAI
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough
from langchain.agents import AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser


tools = [get_current_weather, get_forecast_weather]
functions = [convert_to_openai_function(f) for f in tools]

model = ChatOpenAI(
    model='gpt-4o-mini',
    temperature=0
).bind(functions=functions)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are helpful weather assistant assistant. You will only answer weather related questions"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

agent_chain = RunnablePassthrough.assign(
    agent_scratchpad= lambda x: format_to_openai_functions(x["intermediate_steps"])
) | prompt | model | OpenAIFunctionsAgentOutputParser()

memory = ConversationBufferMemory(return_messages=True,memory_key="chat_history")

agent_executor = AgentExecutor(agent=agent_chain, tools=tools, verbose=True, memory=memory)

print(agent_executor.invoke({"input": "What is the weather like in Oslo?"}))