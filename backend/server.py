import os
from flask import Flask, request, render_template, make_response, jsonify
import requests

app = Flask(__name__)
TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")  # прихований chat_id

@app.route("/", methods=["GET"])
def home():
    msg = request.cookies.get("msg")
    resp = make_response(render_template("index.html", msg=msg))
    resp.set_cookie("msg", "", expires=0)
    return resp

@app.route("/send", methods=["POST"])
def send():
    data = request.json
    text = data.get("text")

    if not text:
        return {"ok": False, "error": "Missing 'text'"}, 400

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    res = requests.post(url, json={"chat_id": CHAT_ID, "text": text})

    if res.ok:
        response = make_response(jsonify({"ok": True}))
        response.set_cookie("msg", "Повідомлення надіслано!", max_age=5)
        return response
    else:
        response = make_response(jsonify({"ok": False}))
        response.set_cookie("msg", "Помилка надсилання!", max_age=5)
        return response, res.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))