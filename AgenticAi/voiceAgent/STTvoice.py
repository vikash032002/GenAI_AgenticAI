import speech_recognition as sr
from openai import OpenAI
from dotenv import load_dotenv
import os
import asyncio
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

openai = AsyncOpenAI()

#text to speech
async def tts(speech:str):
    async with openai.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        input=speech,
        instructions="Speak in a cheerful and positive tone.",
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)


def main():
    r = sr.Recognizer() # speech to text

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 2 

        print("Speak Something...")
        audio = r.listen(source)

        print("Processing Audio...")
        stt = r.recognize_google(audio)

        SYSTEM_PROMPT=f"""
            You are an expert voice agent . What the user will give input audio it will transcript to text.
            Acording to that you will speak.and what ever you speak will be converted to audio via llm.
        """
        response = client.chat.completions.create(
            model='gemini-2.5-flash',
            messages=[
                {'role':'system','content':SYSTEM_PROMPT},
                {'role':'user','content':stt}
            ]
        )

        ai_response = response.choices[0].message.content
        print("you said", stt)
        print("Ai_respone",ai_response)
        asyncio.run(tts(speech=ai_response))

main()
