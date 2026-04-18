from openai import OpenAI
import requests
import json
import os
from dotenv import load_dotenv
import time

# Load env
load_dotenv()

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN"),
)

SYSTEM_PROMPT = """You are Maddy, a strict weather assistant. 
You ONLY answer weather-related questions.

Rules:
- If the user asks anything NOT related to weather → politely refuse.
- Do NOT solve math.
- Do NOT answer general questions.
- For weather queries → use the get_weather tool.
- Never answer weather from your own knowledge. Always use tool."""


# -----------------------------
# 🔧 TOOL: Get Weather
# -----------------------------
def get_weather(city: str):
    try:
        url = f"https://wttr.in/{city}?format=%C+%t"
        res = requests.get(url, timeout=5)

        if res.status_code == 200:
            return {"city": city, "weather": res.text.strip()}
        else:
            return {"error": f"Failed to fetch weather for {city}"}
    except Exception as e:
        return {"error": str(e)}


# -----------------------------
# 🧾 TOOL SCHEMA
# -----------------------------
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather of a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "Name of the city"}
                },
                "required": ["city"],
            },
        },
    }
]


# -----------------------------
# 🤖 AGENT LOOP
# -----------------------------
def run_agent():
    print("🌦️ Welcome! I am Maddy (Real Weather Agent)\n")

    while True:
        user_input = input("👉 Ask Weather: ")

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input},
        ]

        for step in range(5):
            try:
                response = client.chat.completions.create(
                    model="google/gemma-4-31B-it:fastest",
                    messages=messages,
                    tools=tools,
                    tool_choice="auto",
                )
            except Exception as e:
                print("⚠️ API Error:", e)
                time.sleep(5)
                continue

            msg = response.choices[0].message
            # print("response",msg)
            # -----------------------------
            # 🔥 TOOL CALL HANDLING
            # -----------------------------
            if msg.tool_calls:
                tool_call = msg.tool_calls[0]

                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                print(f"🛠️ Calling Tool: {tool_name}({tool_args})")

                if tool_name == "get_weather":
                    result = get_weather(**tool_args)
                else:
                    result = {"error": "Unknown tool"}

                # Add assistant tool call
                messages.append(msg)

                # Add tool response
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result),
                    }
                )

                continue

            # -----------------------------
            # ✅ FINAL OUTPUT
            # -----------------------------
            print("🤖", msg.content)
            break


# -----------------------------
# 🚀 RUN
# -----------------------------
if __name__ == "__main__":
    run_agent()
