import os
import pickle
from datetime import datetime, timedelta


from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
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
    assert cal_id is not None, "Fail to get GOOGLE_CALENDAR_ID"
    assert len(cal_id) > 10, "Invalid cal_id"

    credentials = Credentials.from_service_account_file('service-account.json')
    scoped_credentials = credentials.with_scopes(SCOPES)

    try:
        service = build("calendar", "v3", credentials=scoped_credentials)
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
