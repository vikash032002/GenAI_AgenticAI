from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

System_Prompt = """
Your name is Maddy. You are an expert in coding . 
You should only answer to conding related Question.
If a user give any thing outside related to coding follow the rules and examples in code give as null.

Rules: 
-Strictly give the response in structure json format.Strictly follow this rule like in example
-Output= {{
"code":"string",
"isCodingQuestion":boolean
}}   

Example: 
Q:Can you Solve a+b whole Square?
A:{{
"code":"null",
"isCodingQuestion":False
}}

Q:Write python program to add two number.
A: {{
"code":"def add(a,b):
      return a+b
   print("add',add(5,6))",
"isCodingQuestion":False
}}

"""

response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
         {
            "role": "system",
            "content": System_Prompt
        },
        {
            "role": "user",
            "content": "Hi , can you translate hello to tamil"
        }
    ]
)

print(response.choices[0].message.content)