import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.mongodb import MongoDBSaver

load_dotenv()

DB_URI = os.getenv("MONGO_URI")

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
# state
class State(TypedDict):
    messages: Annotated[list,add_messages]


def format_messages(messages):
    formatted = []

    for msg in messages:
        if msg.type == "human":
            formatted.append({"role": "user", "content": msg.content})
        elif msg.type == "ai":
            formatted.append({"role": "assistant", "content": msg.content})

    return formatted


# creating llm node
def Chatbot(state:State):
    formatted_messages = format_messages(state["messages"])
    response = client.chat.completions.create(
        model="gemini-2.5-flash", 
        messages=formatted_messages
    )

    return{
        "messages":[{
            "role":"assistant",
            "content":response.choices[0].message.content
        }]
    }

# building graph
def build_graph():
    graph = StateGraph(State)

    graph.add_node("chatbot",Chatbot)
    graph.set_entry_point("chatbot")
    graph.add_edge("chatbot",END)

    return graph

# Run with Checkpointer
with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:

    graph = build_graph()

    graph_with_checkpointer = graph.compile(checkpointer=checkpointer)

    config = {"configurable": {"thread_id": "vikash"}}

    print("Type 'exit' to stop\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        for chunk in graph_with_checkpointer.stream(
            {"messages": [{"role": "user", "content": user_input}]},
            config,
            stream_mode="values",
        ):
            print("Bot:", chunk["messages"][-1].content)
