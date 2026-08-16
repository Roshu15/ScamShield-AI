from scam_analyzer import analyze_scam


message = """
Congratulations! You have won ₹5,00,000.
Click this link immediately and enter your UPI PIN
to receive your prize.
"""


result = analyze_scam(message)


print("\n==============================")
print("       SCAMSHIELD RESULT")
print("==============================\n")

print(result)