import os
import pickle
from datetime import datetime, timedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


def dt_to_rfc3339(_dt: datetime) -> str:
    return _dt.strftime("%Y-%m-%dT%H:%M:%S+09:00")


def add(
    title: str,
    body: str,
    begin_date: datetime,
    end_date: datetime,
    cal_id: str | None = os.environ.get("GOOGLE_CALENDAR_ID"),
) -> str:
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    https://developers.google.com/calendar/quickstart/python
    """
    assert cal_id is not None, "Fail to get GOOGLE_CALENDAR_ID"
    assert len(cal_id) > 10, "Invalid cal_id"

    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0, open_browser=False)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)
        event = {
            "summary": title,
            "description": body,
            "start": {
                "dateTime": dt_to_rfc3339(begin_date),
                "timeZone": "Asia/Tokyo",  # 1985-04-12T23:20:50.52Z
            },
            "end": {
                "dateTime": dt_to_rfc3339(end_date),
                "timeZone": "Asia/Tokyo",  # 1985-04-12T23:20:50.52Z
            },
        }
        result = service.events().insert(calendarId=cal_id, body=event).execute()
        return result.get("htmlLink")
    except HttpError as err:
        return str(err)
    


if __name__ == "__main__":
    a = add(
        title="Test schdule",
        body="Test schedule body",
        begin_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=1),
    )
    print(a)
