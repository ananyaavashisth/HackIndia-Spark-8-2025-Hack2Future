import re

HATE_SPEECH_PATTERNS = [
    r"clg\s*(is|was|are|am)\s*(worst|bad|useless|hell|shit|bakwas|bekar)",
    r"hate\s*this\s*college",
    r"ragging",
    r"bully|bullying|bullied",
    r"harass|harassment|harassed",
    r"faculty\s*(is|are)\s*(bad|worst|useless|corrupt)",
    r"management\s*(is|are)\s*(bad|worst|useless|corrupt)",
    r"i\s*was\s*threatened",
    r"i\s*was\s*abused",
    r"i\s*was\s*beaten",
    r"i\s*feel\s*unsafe",
    r"unsafe\s*in\s*college"
    # Add more as needed
]

def detect_hate_speech(message):
    message = message.lower()
    for pattern in HATE_SPEECH_PATTERNS:
        if re.search(pattern, message):
            return True
    return False