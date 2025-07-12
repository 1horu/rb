from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

@app.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"ok": False, "error": "No text provided"}), 400

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}

    try:
        r = requests.post(url, json=payload)
        return jsonify({"ok": r.ok})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
