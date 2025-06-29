import os
import pickle
import pytz
import config

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.events']
CREDENTIALS_FILE = './config/credentials.json'
TOKEN_FILE = './config/token.pickle'


def authenticate_google_calendar():
    creds = None

    if not os.path.exists(CREDENTIALS_FILE):
        print(f"Error: Credentials file '{CREDENTIALS_FILE}' not found. Please provide it.")
        exit(1)

    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        try:
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)
        except Exception as e:
            print(f"Failed to save token: {e}")
            exit(1)

    return creds



def create_calendar_event(low_tide_time, event_start, event_end, tide_height):
    creds = authenticate_google_calendar()
    try:
        service = build('calendar', 'v3', credentials=creds)
    except Exception as e:
        print(f"Failed to build calendar service: {e}")
        exit(1)

    tz = pytz.timezone('Australia/Sydney')

    event = {
        'summary': f"Low Tide Window (Tide Height: {tide_height} @ {low_tide_time.strftime('%H:%M')})",
        'description': f"Lowest tide around {low_tide_time.strftime('%H:%M')}",
        'start': {
            'dateTime': tz.localize(event_start).isoformat(),
            'timeZone': 'Australia/Sydney',
        },
        'end': {
            'dateTime': tz.localize(event_end).isoformat(),
            'timeZone': 'Australia/Sydney',
        },
    }

    attendees = [{'email': email.strip()} for email in config.attendees if email.strip()]
    if attendees:
        event['attendees'] = attendees

    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Event created: {event.get('htmlLink')}")
    except Exception as e:
        print(f"Failed to create event: {e}")
        exit(1)

    return event


