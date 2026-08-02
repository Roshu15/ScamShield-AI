import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from prompts import SCAM_ANALYSIS_PROMPT

load_dotenv()

llm = ChatGroq(
    model = "llama-3.3-70b-versatile" ,
    api_key = os.getenv("GROQ_API_KEY")
)

def analyze_scam(message):
    prompt = SCAM_ANALYSIS_PROMPT.format(
        message = message
    )

    response = llm.invoke(prompt)

    return response.content