import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

# Load PDF
loader = PyPDFLoader("data/phishing.pdf")
docs = loader.load()

# Split text
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(docs)

# Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Vector DB
db = Chroma.from_documents(
    chunks,
    embeddings,
    persist_directory="./chroma_db"
)

retriever = db.as_retriever()

# LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

while True:

    query = input("You: ")

    if query.lower() == "exit":
        break

    docs = retriever.invoke(query)

    context = "\n".join(
        [doc.page_content for doc in docs[:3]]
    )

    prompt = f"""
Use the context below to answer.

Context:
{context}

Question:
{query}
"""

    response = llm.invoke(prompt)

    print("\nBot:", response.content)
    print()