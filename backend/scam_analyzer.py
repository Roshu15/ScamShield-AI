import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


load_dotenv()



# 1. LOAD EMBEDDINGS


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)



# 2. LOAD OUR EXISTING VECTOR DATABASE


db = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)


retriever = db.as_retriever(
    search_kwargs={"k": 4}
)



# 3. CREATE LLM

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY")
)


# 4. SCAM ANALYZER


def analyze_scam(message):

    # Search our trusted knowledge base
    relevant_docs = retriever.invoke(message)

    context = "\n\n".join(
        doc.page_content
        for doc in relevant_docs
    )


    # Ask the LLM to analyze the message
    prompt = f"""
You are ScamShield AI, an AI assistant that helps users
identify possible online scams.

Analyze the following suspicious message using the trusted
knowledge base provided below.

Trusted Knowledge:
{context}

Suspicious Message:
{message}

Your task:

1. Decide the risk level:
   HIGH RISK
   SUSPICIOUS
   or
   LOW RISK

2. Identify the possible scam type.

3. Explain the warning signs found in the message.

4. Give practical safety advice.

5. Do not invent information that is not supported by the
   message or trusted knowledge.

Keep the answer simple and easy for a normal user to understand.

Use this format:

Risk Level:
...

Possible Scam Type:
...

Why It Looks Suspicious:
• ...
• ...
• ...

What You Should Do:
• ...
• ...
• ...
"""


    response = llm.invoke(prompt)

    return response.content