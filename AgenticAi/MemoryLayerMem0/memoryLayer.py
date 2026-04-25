from mem0 import Memory
import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

config = {
    "version": "v1.1",
    "embedder": {
        "provider": "huggingface",
        "config": {
            "model": "multi-qa-MiniLM-L6-cos-v1",
        },
    },
    "llm": {
        "provider": "groq",
        "config": {
            "api_key": GROQ_API_KEY,
            "model": "llama-3.3-70b-versatile",
        },
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333,
            "collection_name": "mem0_vikash",
            "embedding_model_dims": 384,
        },
    },
}

memory_client = Memory.from_config(config)


client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN"),
)

while True:

    user_query = input(">: ")

    # searching from memory_client

    search_memory = memory_client.search(
    query=user_query,
    filters={"user_id": "vikash03"}
    )  # give the result in dictonary type

    memories = [
        f"Id:{mem.get("id")}\nMemory: {mem.get("memory")}" 
        for mem in search_memory.get("results")
    ]

    print("found memory",memories)

    SYSTEM_PROMPTS = f"""
        Here is the context about the user:
        {json.dumps(memories)}

    """

    response = client.chat.completions.create(
        model="google/gemma-4-31B-it:fastest",
        messages=[
            {"role":"system","content":SYSTEM_PROMPTS},
            {"role":"user","content":user_query}
        ]
    )

    ai_response = response.choices[0].message.content

    print("ai_response", ai_response)

    memory_client.add(
        user_id="vikash03",
        messages=[
            {"role":"user","content":user_query},
            {"role":"assistant","content":ai_response}
        ]
    )

    print("Memory Saved.....")
