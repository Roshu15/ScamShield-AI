from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from workflow import process_query


app = FastAPI(
    title="ScamShield AI",
    description="AI powered online scam detection assistant",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "message": "ScamShield AI API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    response = process_query(request.message)

    return {
        "user_message": request.message,
        "response": response
    }