from openai import OpenAI
from dotenv import load_dotenv
import os
from typing import TypedDict
from langgraph.graph import StateGraph, END

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# define state
class ChatState(TypedDict):
    input: str
    output: str

# define nodes
def llm_node(state:ChatState):
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[{"role":"user","content":state["input"]}]
    )

    return {"output":response.choices[0].message.content}

def math_node(state:ChatState):
    try:
        result = eval(state["input"])
        return {"output":f"Math result:{result}"}
    except:
        return{"output":"Invalid math expression"}

def router_node(state:ChatState):
    return state

def decide_route(state:ChatState):
    text = state["input"]

    if any(char.isdigit() for char in text ):
        return "math"

    return "llm"


def check_math_result(state: ChatState):
    if "Invalid math expression" in state["output"]:
        return "llm"
    return "end"


# building graph
graph = StateGraph(ChatState)

# adding nodes

graph.add_node("router", router_node)
graph.add_node("llm",llm_node)
graph.add_node("math",math_node)

# entry point
graph.set_entry_point("router")

# conditional edges

graph.add_conditional_edges(
    "router",
    decide_route,
    {
        "llm":"llm",
        "math":"math"
    }
)

graph.add_conditional_edges("math", check_math_result, {"llm": "llm", "end": END})

# add edges

graph.add_edge("llm",END)
# graph.add_edge("math",END)

# compiling of graph
app = graph.compile()

# invoke into graph

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    result = app.invoke({"input": user_input})

    print("Bot:", result["output"])
