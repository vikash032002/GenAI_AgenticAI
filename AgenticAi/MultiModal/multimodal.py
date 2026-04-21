from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://apod.nasa.gov/apod/image/2604/TripleArchAlps_Fux_7500.jpg"
                    },
                },
            ],
        }
    ],
)

print(response.choices[0].message.content)

# models = client.models.list()

# for m in models.data:
#     print(m.id)
