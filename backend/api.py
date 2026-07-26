from fastapi import FastAPI
from workflow import is_scam_query, rag_response, normal_response

app = FastAPI()

@app.get("/")
def home():
    return {
        "message" : "ScamShield AI API Running"
    }

@app.post("/chat")
def chat(request: dict):
    query = request["question"]

    if is_scam_query(query):
        answer = rag_response(query)

    else:
        answer = normal_response(query)

    return {
        "question" : query,
        "answer" : answer
    }