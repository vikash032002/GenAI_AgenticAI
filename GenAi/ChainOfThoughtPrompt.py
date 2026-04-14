from openai import OpenAI
from dotenv import load_dotenv
import json
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = """
Your Name is Maddy.
You are an expert Ai Assitant resolving Query using Chain of thought process.
Your Steps are START | PLAN | OUTPUT

Rules:
- Strictly follow the given json format to give the output.
- Only runs one steps at a time 
- the sequence of steps will be like Start ( Where the user will give input),Plan(where the llm will think  to give the perfect solution)
  after planning the next step will be the OUTPUT(Where you give the solution of the query) 
- only give the structured json format and dont give all the setps together give it one by one in json format
-"solve step by step and return JSON"

Output JSON Format:
  {"step":"START" | "PLAN" | "OUTPUT" , "content":"string"}

Example:
START:Hey, Can you solve 2+3*4/2?
PLAN:{"step":"PLAN","content":"Seems like this is maths problem. We can solve this using BODMAS rule. First we will divide 4/2 which is 2 . then we multiply 3*2 which is 6. Now we will add 2+6 which will be 8"}
OUTPUT:{"step":"OUTPUT","content":"So this problem is solved and the final output is 8"}

"""

# Example:
# START:Hey, Can you solve 2+3*4/2?
# PLAN:{"step":"PLAN","content":"Seems like this is maths problem"}
# PLAN:{"step":"PLAN","content":"We can solve this using BODMAS rule"}
# PLAN:{"step":"PLAN","content":"First we will divide 4/2 which is 2"}
# PLAN:{"step":"PLAN","content":"then we multiply 3*2 which is 6"}
# PLAN:{"step":"PLAN","content":"Now we will add 2+6 which will be 8"}
# OUTPUT:{"step":"OUTPUT","content":"So this problem is solved and the final output is 8"}

print("Welcome to MaddyAi. How can i help You? \n\n\n")

user_Query = input("👉Write Query:")

message_History=[{
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_Query
        },
        ]

while True:
    response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    response_format={ "type": "json_object" },
    messages=message_History
     )
    
    result = response.choices[0].message.content
    message_History.append({
        "role":"assistant",
        "content":result
    })
    parse_result = json.loads(result)
    # print(parse_result)

    if parse_result.get("step") == "START":
        print("🔥",parse_result.get("content"))
        continue

    if parse_result.get("step") == "PLAN":
        print("🧠💭",parse_result.get("content"))
        continue

    if parse_result.get("step") == "OUTPUT":
        print("🤖 Output: ",parse_result.get("content"))
        break


print("\n\n\n")