from flask import Flask, request, jsonify
import requests, os, cv2, numpy as np
from PIL import Image

BOT_TOKEN = "7240415432:AAFAS5koSCfWdaLKy6M0U2PMQqBg9OWX1ig"
CHAT_ID = "5834718648"

app = Flask(__name__)

def send_message(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)

def analyze_image(image_path):
    img = cv2.inread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    structure_score = len(contours)
    trend_score = 0

    lower_blue = np.array([100, 0, 0])
    upper_blue = np.array([255, 150, 150])
    mask_blue = cv2.inRange(img, lower_blue, upper_blue)
    if cv2.countNonZero(mask_blue) > 200:
        trend_score += 1

    lower_yellow = np.array([0, 200, 200])
    upper_yellow = np.array([150, 255, 255])
    mask_yellow = cv2.inRange(img, lower_yellow, upper_yellow)
    if cv2.countNonZero(mask_yellow) > 200:
        trend_score += 1

    entry = 105750.0
    sl = entry - 0.003 * entry
    tp1 = entry + 0.005 * entry
    tp2 = entry + 0.008 * entry
    rr = round((tp1 - entry) / (entry - sl), 2)

    if trend_score == 2 and structure_score > 10:
        confidence = "🔥 HIGH"
    elif trend_score >= 1:
        confidence = "⚠️ MID"
    else:
        confidence = "❌ LOW"

    message = (
        f"📸 Screenshot Analyse Ergebnis:\n\n"
        f"📈 Trend: {'EMA erkannt' if trend_score > 0 else 'Keine EMA erkannt'}\n"
        f"📐 Struktur: {structure_score} Zonen gefunden\n\n"
        f"📍 Entry: {round(entry, 2)}\n"
        f"🛑 SL: {round(sl, 2)}\n"
        f"🎯 TP1: {round(tp1, 2)} | TP2: {round(tp2, 2)}\n"
        f"📊 R:R ≈ {rr}\n"
        f"🧠 Confidence: {confidence}\n"
        f"#TRADINGCORE™ Visual AI"
    )

    return message

@app.route(f"/bot{BOT_TOKEN}/", methods=["POST"])
def telegram_photo_handler():
    data = request.json

    if "message" in data and "photo" in data["message"]:
        file_id = data["message"]["photo"][-1]["file_id"]
        file_info = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}").json()
        file_path = file_info["result"]["file_path"]
        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
        img_data = requests.get(file_url).content

        filename = "incoming_screenshot.png"
        with open(filename, "wb") as f:
            f.write(img_data)

        msg = analyze_image(filename)
        send_message(msg)
        os.remove(filename)
        return jsonify({"status": "analyzed"})

    return jsonify({"status": "no_photo"})

@app.route('/')
def root():
    return jsonify({"status": "TRADINGCORE™ V2 ONLINE ✅"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
