import datetime
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('/src/token.json'):
        creds = Credentials.from_authorized_user_file('/src/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/src/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('/src/token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


class Interface:
    def __init__(self):
        self.credentials = get_credentials()
        self.service = build('calendar', 'v3',
                             credentials=self.credentials,
                             developerKey=os.environ.get("GOOGLE_API_KEY"))

    def create_event(self,
                     datetime_start: datetime.datetime,
                     datetime_end: datetime.datetime,
                     max_height: str,
                     appears: str,
                     disappears: str):

        event_id = generate_event_id(datetime_start)

        event = {
            'summary': 'ISS Overhead',
            'id': event_id,
            'location': 'Burnaby, BC',
            'description': f'Max Height: {max_height}\n'
                           f'Appears: {appears}\n'
                           f'Disappears: {disappears}',
            'start': {
                'dateTime': to_api_datetime(datetime_start),
                'timeZone': 'America/Vancouver',
            },
            'end': {
                'dateTime': to_api_datetime(datetime_end),
                'timeZone': 'America/Vancouver',
            },
            'reminders': {
                'useDefault': True,
            },
        }

        try:
            event = self.service.events().insert(calendarId='primary', body=event).execute()

        except HttpError as error:
            print(error)

    def check_for_event(self, date: datetime.datetime) -> bool:
        try:

            event_id = generate_event_id(date)

            # Call the Calendar API
            event = self.service.events().get(calendarId='primary', eventId=event_id).execute()
            # print(event)
            return event is None

        except HttpError as error:
            print(error)
            return None

    def delete_event(self, start_timestamp):
        self.service.events().delete(calendarId='primary', eventId=generate_event_id(start_timestamp)).execute()


def generate_event_id(date: datetime.datetime) -> str:
    iteration = 8
    return date.strftime("issoverhead%Y%m%d")


def to_api_datetime(date: datetime.datetime) -> str:
    return date.strftime("%Y-%m-%dT%H:%M:00-07:00")
