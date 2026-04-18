from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
import json
from pydantic import BaseModel, Field
from typing import Optional

load_dotenv()

print("Welcome ! I am Maddy Your Weather buddy")
# client = OpenAI(
#     api_key=os.getenv("GEMINI_API_KEY"),
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

# Hugging Face Ai setup
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN"),
)

SYSTEM_PROMPT = """
Your Name is Maddy Weather Agent.
You are an expert Ai Assitant resolving Query using Chain of thought process.
Your Steps are START | PLAN | TOOL | OUTPUT |

Rules:
- Strictly follow the given json format to give the output.
- Only runs one steps at a time 
- the sequence of steps will be like Start ( Where the user will give input),Plan(where the llm will think  to give the perfect solution)
  after planning the next step will be the TOOL(where you use the tool to get the input) OUTPUT(Where you give the solution of the query) 
- only give the structured json format and dont give all the setps together give it one by one in json format
-"solve step by step and return JSON"
- if from the avilable tool you wont get real data then dont give output by your own beside you can write There some problem with tool try again later .

avilable_tools = {
    "get_Weather":get_Weather
}

Output JSON Format:
  {"step":"START" | "PLAN" | "OUTPUT" , "content":"string" , "tool":"string" , "input":"string"}

Example:
START:Hey, Whats the Weather of Chennai?
PLAN:{"step":"PLAN","content":"Seems like user wants the weather of chennai . Lets check whether any tools are avilable to get_weather or not > Great we have get_Weather tool present."}
TOOL:{"step":"TOOL","tool":"get_Weather","input":"Chennai"}
- if from the avilable tool you wont get real data then dont give output by your own beside you can write There some problem with tool try again later .
OUTPUT:{"step":"OUTPUT","content":"The temperatre of Chennai is partially cloudy with 38°C"}

"""


class StructureOutput(BaseModel):
    step: str = Field(
        ..., description="The id of the step.it can be PLAN,OUTPUT,TOOL,START..etc"
    )
    tool: Optional[str] = Field(None, description="the id of the tool to call")
    content: Optional[str] = Field(None, description="the optional string content")
    input: Optional[str] = Field(None, description="the input params of tool")


def get_Weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        print(f"The Wearther of in {city} is {response.text}")
        return f"The Wearther of in {city} is {response.text}"


avilable_tools = {"get_Weather": get_Weather}


while True:
    user_Query = input("👉Write Query:")

    message_History = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_Query},
    ]

    while True:
        response = client.chat.completions.parse(
            model="google/gemma-4-31B-it:fastest",
            response_format=StructureOutput,
            messages=message_History,
        )

        result = response.choices[0].message.content
        message_History.append({"role": "assistant", "content": result})
        parse_result = response.choices[0].message.parsed
        # print(f"llm response{parse_result}")

        if parse_result.step == "START":
            print("🔥", parse_result.content)
            continue

        if parse_result.step == "PLAN":
            print("🧠💭", parse_result.content)
            continue

        if parse_result.step == "TOOL":
            tool_toCall = parse_result.tool
            tool_input = parse_result.input
            # print(f"test{tool_toCall}:{tool_input}")
            tool_response = avilable_tools[tool_toCall](tool_input)
            message_History.append(
                {
                    "role": "tool",
                    "content": json.dumps(
                        {"city": tool_input, "weather": tool_response}
                    ),
                }
            )
            continue

        if parse_result.step == "OUTPUT":
            print("🤖 Output: ", parse_result.content)
            break
