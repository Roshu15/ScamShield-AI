from scam_analyzer import analyze_scam


test_messages = [
    "Someone called saying they are from the police and that I will be arrested unless I transfer ₹50000.",

    "I received a message saying I won ₹2 lakh and I need to enter my UPI PIN to receive the money.",

    "A person claiming to be customer support asked me to install an app and give remote access to my phone."
]


for message in test_messages:

    print("\n" + "=" * 70)
    print("MESSAGE:")
    print(message)
    print("=" * 70)

    result = analyze_scam(message)

    print("\nSCAMSHIELD AI ANALYSIS:\n")
    print(result)