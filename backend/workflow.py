from rag_chatbot import ask_question
from scam_analyzer import analyze_scam


def process_query(user_input):

    scam_keywords = [
        "otp",
        "bank",
        "upi",
        "click",
        "link",
        "won",
        "prize",
        "gift",
        "urgent",
        "refund",
        "cashback",
        "verify",
        "password",
        "account"
    ]

    text = user_input.lower()

    if any(keyword in text for keyword in scam_keywords):
        return analyze_scam(user_input)

    return ask_question(user_input)


if __name__ == "__main__":

    print("=" * 50)
    print("        ScamShield AI")
    print("=" * 50)

    while True:

        user_input = input("\nYou : ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        response = process_query(user_input)

        print("\nBot:\n")
        print(response)