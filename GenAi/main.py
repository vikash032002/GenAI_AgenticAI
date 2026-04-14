from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    messages=[
         {
            "role": "system",
            "content": "You are a expert Ai assitant"
        },
        {
            "role": "user",
            "content": "Hi Vikash this side"
        }
    ]
)

print(response.choices[0].message.content)