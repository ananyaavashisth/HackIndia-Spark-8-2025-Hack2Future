from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def get_google_creds():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return creds

def create_google_calendar_event(event, dt):
    creds = get_google_creds()
    service = build('calendar', 'v3', credentials=creds)
    event_body = {
        'summary': event,
        'start': {'dateTime': dt.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': (dt + timedelta(hours=1)).isoformat(), 'timeZone': 'Asia/Kolkata'},
    }
    created_event = service.events().insert(calendarId='primary', body=event_body).execute()
    return created_event.get('htmlLink')