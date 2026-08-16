import os
import json

from dotenv import load_dotenv

from langchain_groq import ChatGroq

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_core.documents import Document


load_dotenv()



# 1. LOAD PDF


loader = PyPDFLoader("data/phishing.pdf")

docs = loader.load()



# 2. LOAD JSON DATASET


with open(
    "data/scam_knowledge.json",
    "r",
    encoding="utf-8"
) as file:

    scam_data = json.load(file)



# 3. CONVERT JSON TO LANGCHAIN DOCUMENTS


json_docs = []


for item in scam_data:

    content = f"""
Scam Type: {item['type']}

Description:
{item['description']}

Warning Signs:
{', '.join(item['warning_signs'])}

Safety Recommendations:
{', '.join(item['safety'])}

Source:
{item['source']}
"""

    json_docs.append(
        Document(
            page_content=content,
            metadata={
                "source": item["source"],
                "scam_type": item["type"]
            }
        )
    )



# 4. COMBINE PDF + JSON


all_docs = docs + json_docs



# 5. SPLIT DOCUMENTS


splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(all_docs)



# 6. CREATE EMBEDDINGS


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)



# 7. CREATE VECTOR DATABASE


db = Chroma.from_documents(
    chunks,
    embeddings,
    persist_directory="./chroma_db"
)

retriever = db.as_retriever(
    search_kwargs={"k": 4}
)



# 8. CREATE LLM


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)



# 9. QUESTION FUNCTION


def ask_question(query):

    relevant_docs = retriever.invoke(query)

    context = "\n\n".join(
        doc.page_content
        for doc in relevant_docs
    )

    prompt = f"""
You are ScamShield AI, an online scam awareness assistant.

Use the provided context to answer the user's question.

Do not invent information.

If the context does not contain enough information,
say that the information is not available in the
current knowledge base.

Context:
{context}

User Question:
{query}

Give a clear and simple answer.
"""

    response = llm.invoke(prompt)

    return response.content



# 10. TERMINAL CHAT


if __name__ == "__main__":

    print("================================")
    print("       ScamShield AI")
    print("================================")
    print("Type 'exit' to stop.")

    while True:

        query = input("\nYou: ")

        if query.lower() == "exit":
            break

        answer = ask_question(query)

        print("\nBot:", answer)
        