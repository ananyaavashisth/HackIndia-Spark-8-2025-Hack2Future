from datetime import datetime, timedelta
# from googleapiclient.discovery import build
# from google.oauth2.credentials import Credentials

def create_reminder(text, time_str):
    # Dummy implementation: In production, use Google Calendar API and OAuth2
    # Parse time_str to datetime, here we just add 1 hour for demo
    start_time = datetime.now() + timedelta(hours=1)
    end_time = start_time + timedelta(hours=1)
    # creds = get_google_creds()
    # return add_event_to_calendar(text, start_time.isoformat(), end_time.isoformat(), creds)
    return f"Reminder set for {text} at {start_time.strftime('%Y-%m-%d %H:%M')} (Demo only)"