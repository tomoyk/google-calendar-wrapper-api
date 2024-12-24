# Google Calendar Wrapper API

## Getting started (local debug)

1. Get access token from Google Cloud console

https://console.cloud.google.com/apis/api/calendar-json.googleapis.com/overview

2. Set Google Calendar ID as an environment variable

```
export GOOGLE_CALENDAR_ID="xxx"
```

3. Dry-run google_calendar.py

```
python google_calendar.py
```

4. Start HTTP server

```
python main.py
```

4. Send an HTTP request to the server

```
curl -XPOST -u koyama:pA55word -H 'Content-Type: application/json' \
  -d '{"title": "test1", "body": "2024-12-24の12:00から14:00"}' 'http://localhost:8080/v1/schedule'
```

## Deploy to Cloud Run

https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service?hl=ja

