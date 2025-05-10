import re

# List of English and Hindi phrases for tiredness, sleepiness, headache, etc.
CHAI_BREAK_PHRASES = [
    r"i\s*[' ]*am\s*tired",
    r"i\s*[' ]*am\s*sleepy",
    r"i\s*[' ]*want\s*a\s*break",
    r"mai\s*thak\s*gya\s*yaar",
    r"thak\s*gya",
    r"neend\s*aa\s*rhi\s*h",
    r"sar\s*dard\s*kr\s*rha\s*h",
    r"headache\s*ho\s*rha\s*h",
    r"headache",
    r"tired",
    r"sleepy",
    r"break",
    r"thak\s*gayi",
    r"mai\s*thak\s*gayi\s*hoon",
    r"neend\s*aa\s*rhi\s*hai",
    r"sar\s*dard",
    r"thaka\s*hua",
    r"thak\s*chuka\s*hoon",
    r"thak\s*chuki\s*hoon"
]

def detect_chai_break(message):
    message = message.lower()
    for pattern in CHAI_BREAK_PHRASES:
        if re.search(pattern, message):
            return "You seem tired! Take a chai break ☕"
    return None