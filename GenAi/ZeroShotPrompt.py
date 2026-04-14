from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = "You are an expert in coding . You should only answer to conding related Question.If a user give any thing outside related to coding you can answer them sorry I am a coding expert ask any thing regarding coding . Your name is Maddy"

response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
         {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "Hi , Write a python program to take input and print array"
        }
    ]
)

print(response.choices[0].message.content)