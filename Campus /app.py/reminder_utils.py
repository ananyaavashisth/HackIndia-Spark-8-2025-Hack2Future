import dateparser
import re

def parse_reminder(message):
    # Example: "Remind me of my project meeting tomorrow at 3 PM"
    # Extract event description and datetime
    match = re.search(r"remind me (?:of|about|to)? (.+?)(?: on| at|$)", message, re.IGNORECASE)
    event = match.group(1).strip() if match else message
    # Use dateparser to find date/time
    dt = dateparser.parse(message, settings={'PREFER_DATES_FROM': 'future'})
    return event, dt