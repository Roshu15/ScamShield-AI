from scam_analyzer import analyze_scam


def run_workflow(message):

    """
    Main ScamShield AI workflow.

    User message
        ↓
    Scam Analyzer
        ↓
    RAG knowledge base
        ↓
    Final scam analysis
    """

    if not message or not message.strip():

        return {
            "success": False,
            "message": "Please enter a message to analyze."
        }

    result = analyze_scam(message)

    return {
        "success": True,
        "message": message,
        "analysis": result
    }


# ==========================================
# TEST WORKFLOW
# ==========================================

if __name__ == "__main__":

    test_message = """
    Congratulations! You have won ₹5,00,000.
    Click this link immediately and enter your UPI PIN
    to receive your prize.
    """

    result = run_workflow(test_message)

    print("\n==============================")
    print("       SCAMSHIELD WORKFLOW")
    print("==============================\n")

    print(result["analysis"])