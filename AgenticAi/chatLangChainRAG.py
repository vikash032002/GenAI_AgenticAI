from dotenv import load_dotenv
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
import os

load_dotenv()

# load the data from vector db qdrant
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

vector_store = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url="http://localhost:6333/",
    collection_name="LangChainRAG",
)

# taking user query and matching the similarity from vectorDB

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN"),
)
while True:
    user_query = input("Query: ")

    search_result = vector_store.similarity_search(query=user_query)

    # now passing this result to model to get the exact data from file

    context = "\n\n\n".join(
        [
            f"Page Content: {result.page_content}\n"
            f"Page Number: {result.metadata.get('page_label', 'N/A')}\n"
            f"File Location: {result.metadata.get('source', 'N/A')}"
            for result in search_result
        ]
    )

    SYSTEM_PROPMTS = f"""
You are a helpful AI assistant who anser user Query based on the avilable context retrived
from the pdf file along with page_content and page number.

You should only answer the user based on the following contex and navigate the user to open right 
page numbe to know more , and give the sumarize and perfect answer fro user query.

Context:{context}
"""

    response = client.chat.completions.create(
        model="google/gemma-4-31B-it:fastest",
        messages=[
            {"role": "system", "content": SYSTEM_PROPMTS},
            {"role": "user", "content": user_query},
        ],
    )

    print("🤖 : ", response.choices[0].message.content)
