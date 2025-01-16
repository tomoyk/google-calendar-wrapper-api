import os

from flask import Flask, request
from flask_httpauth import HTTPBasicAuth

import google_calendar
import parse_text

app = Flask(__name__)
auth = HTTPBasicAuth()


@app.route("/")
def root():
    name = os.environ.get("NAME", "World")
    return f"Hello {name}!"


@auth.get_password
def get_password(username):
    if username == os.environ.get("AUTH_USER", "koyama"):
        return os.environ.get("AUTH_PASSWORD", "pA55word")
    return None


@app.route("/v1/schedule", methods=["POST"])
@auth.login_required
def create():
    title = request.json["title"]
    body = request.json["body"]
    if len(title) < 1:
        return {"result": "failed", "message": "Invalid title length"}, 400
    if len(body) < 5:
        return {"result": "failed", "message": "Invalid body length"}, 400

    begin, end = parse_text.get_datetime_str(text=body)
    if begin is None or end is None:
        return {"result": "failed", "message": "Failed to parse datetime"}, 200

    url = google_calendar.add(
        title=title,
        body=body,
        begin_date=begin,
        end_date=end,
    )
    return {"result": "success", "message": url}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
