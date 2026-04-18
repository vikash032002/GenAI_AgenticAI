from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
# Indexing of RAG
# loading the file docs
file_path = Path(__file__).parent / "SystemDesign.pdf"
loader = PyPDFLoader(file_path)

docs = loader.load()
# print(docs[5])

# Chunking - splitting into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400)

chunks = text_splitter.split_documents(documents=docs)

# embedding then storing to vector database - i am using hugging face sentence transformer for embending
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# vector db i am using qdrant db
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model, 
    url="http://localhost:6333/",
    collection_name="LangChainRAG"
)

print("Indexing Done..")
