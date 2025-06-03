from flask import Flask, request, jsonify
import requests

BOT_TOKEN = "7240415432:AAG4eIKwdi4L2asfY7KDY5Z8fGGV1nfsRVU"
CHAT_ID = "5834718648"

app = Flask(__name__)

@app.route(f"/bot{BOT_TOKEN}/", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    print("📥 RAW DATA:", data)

    if "message" in data and "photo" in data["message"]:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={
                "chat_id": CHAT_ID,
                "text": "✅ Screenshot empfangen!"
            }
        )

    return jsonify({"status": "received"})

@app.route('/')
def home():
    return jsonify({"status": "TRADINGCORE™ LIVE ✅"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
