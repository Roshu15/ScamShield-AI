import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

print("AI Digital Safety Assistant")
print("Type exit to quit\n")

while True:

    query = input("You : ")

    if query.lower() == "exit":
        break

    response = llm.invoke(
        [HumanMessage(content=query)]
    )

    print("\nBot :", response.content)
    print()