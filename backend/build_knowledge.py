import json
from langchain_core.documents import Document

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma



with open("data/scam_knowledge.json", "r", encoding="utf-8") as file:
    scam_data = json.load(file)


json_documents = []

for item in scam_data:

    content = f"""
Scam Category: {item['category']}

Description:
{item['description']}

Warning Signs:
{', '.join(item['warning_signs'])}

Safety Advice:
{', '.join(item['safety_advice'])}

Source:
{item['source']}
"""

    json_documents.append(
        Document(
            page_content=content,
            metadata={
                "category": item["category"],
                "source": item["source"],
                "type": "scam_knowledge"
            }
        )
    )



loader = PyPDFLoader("data/phishing.pdf")

pdf_documents = loader.load()

for doc in pdf_documents:
    doc.metadata["type"] = "pdf"


documents = json_documents + pdf_documents

print(f"JSON documents loaded: {len(json_documents)}")
print(f"PDF pages loaded: {len(pdf_documents)}")
print(f"Total documents: {len(documents)}")



splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)

print(f"Total chunks created: {len(chunks)}")



embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


db = Chroma.from_documents(
    chunks,
    embeddings,
    persist_directory="./chroma_db"
)

print("Knowledge base successfully created!")
print("PDF + scam_knowledge.json are now available to RAG.")

