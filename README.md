# Google Calendar Wrapper API

## About

Google Calendar Wrapper API creates a schedule with natural language in Japanese.
This script provides RESTful API interface and enables integrations for some tools.

One usecase is to use this with iOS shortcuts.

<img src="assets/demo.gif" width="400">

<img src="assets/schedule-dtail.jpg" width="400">

The configuration of iOS shortcut is here.

<img src="assets/shortcut1.jpg" width="350"> <img src="assets/shortcut2.jpg" width="350">

## Getting started (local debug)

1. Get access token from Google Cloud console

https://console.cloud.google.com/apis/api/calendar-json.googleapis.com/overview

2. Install packages

```
python -m venv env
. env/bin/activate
pip install -r requirements.txt
```

3. Set Google Calendar ID as an environment variable

```
export GOOGLE_CALENDAR_ID="xxx"
```

4. Dry-run google_calendar.py

This script creates a schedule on the Google Calendar.

```
python google_calendar.py
```

5. Start HTTP server

```
python main.py
```

6. Send an HTTP request to the server

```
curl -XPOST -u koyama:pA55word -H 'Content-Type: application/json' \
  -d '{"title": "test1", "body": "2024-12-24の12:00から14:00"}' 'http://localhost:8080/v1/schedule'
```

## Deployment

1. Create venv

```
python -m venv env
. env/bin/activate
```

2. Install packages

```
pip install -r requirements.txt
```

3. Dry-run google_calendar.py

```
python google_calendar.py
```

4. Start the app server

```
AUTH_USER=xxx AUTH_PASSWORD=xxx gunicorn main:app --bind 0.0.0.0:8080
```

## Deployment with systemd

1. Add the `gcalapi` user

```
sudo useradd -s /bin/bash gcalapi
```

2. Write `.env-vars` on the project root

```
cat <<EOF > .env-vars
AUTH_USER=xxx
AUTH_PASSWORD=xxx
GOOGLE_CALENDAR_ID=xxx@example.com
EOF
```

3. Edit `gcalapi.service`

```
WorkingDirectory=/path/to
ExecStart=/path/to/env/bin/gunicorn main:app --bind 127.0.0.1:8080
EnvironmentFile=/path/to/.env-vars
```

4. Copy the `gcalapi.service` file

```
sudo install gcalapi.service /etc/systemd/system/
```

5. Apply the service

```
sudo systemctl daemon-reload
sudo systemctl start gcalapi
sudo systemctl enable gcalapi
```

6. Check logs

```
sudo systemctl status gcalapi
```

7. Start NGINX as a proxy

```
sudo apt install nginx
sudo ./nginx.conf /etc/nginx/conf.d/
sudo nginx -t 
sudo systemctl start nginx
sudo systemctl enable nginx
```
