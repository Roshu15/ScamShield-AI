import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

llm = ChatGroq(
    model = "llama-3.3-70b-versatile",
    api_key = os.getenv("GROQ_API_KEY")
)

loader = PyPDFLoader("data/phishing.pdf")
documents = loader.load()


splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 50
)

chunks = splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma.from_documents(
    chunks,
    embeddings
)

retriever = db.as_retriever()

def is_scam_query(query):
    keywords = ["phishing" , "otp" , "upi" , "bank" , "fraud" , "scam" , "cyber" , "link" , "email" , "sms"]

    query = query.lower()

    return any(word in query for word in keywords)

def rag_response(query):
    docs = retriever.invoke(query)

    context = "\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
Answer using the following context.

Context:
{context}

Question:
{query}
"""
    return llm.invoke(prompt).content

def normal_response(query):
    return llm.invoke(query).content

print("ScamShield AI")
print("Type exit to quit\n")

while True:
    query = input("You : ")

    if query.lower() == "exit":
        break

    if is_scam_query(query):
        print("\nUsing RAG Workflow...\n")
        answer = rag_response(query)

    else:
        print("\nUsing General AI...\n")
        answer = normal_response(query)

    print("Bot :" , answer)
    print()