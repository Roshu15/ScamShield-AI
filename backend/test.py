from scam_analyzer import analyze_scam

message = """
Congratulations!

You won ₹25,000.

Click below.

http://bit.ly/abcd
"""

print(analyze_scam(message))