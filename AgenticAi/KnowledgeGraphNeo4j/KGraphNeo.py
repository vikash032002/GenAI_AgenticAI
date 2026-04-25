from mem0 import Memory
from neo4j import GraphDatabase
import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# =========================
# ENV VARIABLES
# =========================
HF_TOKEN = os.getenv("HF_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# =========================
# MEM0 CONFIG (VECTOR)
# =========================
config = {
    "version": "v1.1",
    "embedder": {
        "provider": "huggingface",
        "config": {
            "model": "multi-qa-MiniLM-L6-cos-v1",  # 384 dim
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

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))


def store_graph(user_id, user_msg, ai_msg):
    with driver.session() as session:
        session.run(
            """
            MERGE (u:User {id: $user_id})
            
            CREATE (um:Message {text: $user_msg, role: 'user'})
            CREATE (am:Message {text: $ai_msg, role: 'assistant'})
            
            MERGE (u)-[:SAID]->(um)
            MERGE (u)-[:RECEIVED]->(am)
            """,
            user_id=user_id,
            user_msg=user_msg,
            ai_msg=ai_msg,
        )


def fetch_graph_memory(user_id):
    with driver.session() as session:
        result = session.run(
            """
            MATCH (u:User {id: $user_id})-[:SAID]->(m:Message)
            RETURN m.text AS message
            ORDER BY m.text DESC
            LIMIT 5
            """,
            user_id=user_id,
        )
        return [record["message"] for record in result]


client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)

while True:
    user_query = input(">: ")

    # -------- VECTOR MEMORY --------
    search_memory = memory_client.search(
        query=user_query, filters={"user_id": "vikash03"}
    )

    vector_memories = [
        f"{mem.get('memory')}" for mem in search_memory.get("results", [])
    ]

    # -------- GRAPH MEMORY --------
    graph_memories = fetch_graph_memory("vikash03")

    print("\nVector Memory:", vector_memories)
    print("Graph Memory:", graph_memories)

    # -------- SYSTEM PROMPT --------
    SYSTEM_PROMPTS = f"""
    User Context (Vector Memory):
    {json.dumps(vector_memories)}

    User Context (Graph Memory):
    {json.dumps(graph_memories)}
    """

    # -------- LLM CALL --------
    response = client.chat.completions.create(
        model="google/gemma-4-31B-it:fastest",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPTS},
            {"role": "user", "content": user_query},
        ],
    )

    ai_response = response.choices[0].message.content
    print("\nAI:", ai_response)

    # -------- STORE MEMORY --------
    memory_client.add(
        user_id="vikash03",
        messages=[
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": ai_response},
        ],
    )

    store_graph("vikash03", user_query, ai_response)

    print("\nMemory Saved (Vector + Graph)\n")
