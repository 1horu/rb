import os
from flask import Flask, request
import requests

app = Flask(__name__)
TOKEN = os.environ.get("TOKEN")

@app.route("/", methods=["GET"])
def home():
    return "Server is running"

@app.route("/send", methods=["POST"])
def send():
    data = request.json
    text = data.get("text")
    chat_id = data.get("chat_id")

    if not all([text, chat_id]):
        return {"ok": False, "error": "Missing 'text' or 'chat_id'"}, 400

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    res = requests.post(url, json={"chat_id": chat_id, "text": text})
    return res.json(), res.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))