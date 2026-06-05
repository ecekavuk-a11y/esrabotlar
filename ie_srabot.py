import requests
import json
import time
import sys

BOT_TOKEN = "8280594775:AAEGjZN1nC-YxKUNLVGXufX5Lz2UuGXAsj4"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

CHANNELS = [
    {"name": "📌 Kanal 1 — KATIL", "url": "https://t.me/+92DdkxKLeo9iZTc0"},
    {"name": "📌 Kanal 2 — KATIL", "url": "https://t.me/+33ZaHH-6QIU0ZDY0"},
    {"name": "📌 Kanal 3 — KATIL", "url": "https://t.me/+6v3NjULvEtE2ZWE0"},
    {"name": "📌 Kanal 4 — KATIL", "url": "https://t.me/+QLF_9uRc-NMwMjU8"},
]

WELCOME_TEXT = """┌─────────────────────────────┐
│  🎁 İE'SRA VIP BOT 🎁
└─────────────────────────────┘

Hoşgeldin! 👋

🎁 Sürpriz hediye kazanmak için:

1️⃣ Aşağıdaki TÜM kanallara katıl
2️⃣ Katıldıktan sonra "✅ Kontrol Et" butonuna bas
3️⃣ Hediyeni al! 🎉

⚠️ Tüm kanallara katılmadan hediye verilmez!
⏰ Sınırlı süre!"""

SUCCESS_TEXT = "Şimdi Esra dan gelecek süprizi bekle…😍"

session = requests.Session()
session.headers.update({"Content-Type": "application/json"})


def send_request(method, data=None):
    for attempt in range(3):
        try:
            r = session.post(f"{API_URL}/{method}", json=data, timeout=35)
            return r.json()
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] Hata ({method}, deneme {attempt+1}): {e}", flush=True)
            time.sleep(2)
    return None


def get_welcome_keyboard():
    keyboard = []
    for ch in CHANNELS:
        keyboard.append([{"text": ch["name"], "url": ch["url"]}])
    keyboard.append([{"text": "✅ Kontrol Et — Hediyemi Al!", "callback_data": "check_join"}])
    return {"inline_keyboard": keyboard}


def send_welcome(chat_id):
    data = {
        "chat_id": chat_id,
        "text": WELCOME_TEXT,
        "reply_markup": get_welcome_keyboard()
    }
    result = send_request("sendMessage", data)
    if result and result.get("ok"):
        print(f"[{time.strftime('%H:%M:%S')}] Hoş geldin gönderildi: {chat_id}", flush=True)
    else:
        print(f"[{time.strftime('%H:%M:%S')}] Hoş geldin BAŞARISIZ: {chat_id} - {result}", flush=True)


def handle_callback(callback_query):
    chat_id = callback_query["message"]["chat"]["id"]
    callback_id = callback_query["id"]
    data = callback_query.get("data", "")

    if data == "check_join":
        send_request("answerCallbackQuery", {
            "callback_query_id": callback_id,
            "text": "Kontrol ediliyor..."
        })
        send_request("sendMessage", {
            "chat_id": chat_id,
            "text": SUCCESS_TEXT
        })
        print(f"[{time.strftime('%H:%M:%S')}] Kontrol Et tıklandı: {chat_id}", flush=True)


def handle_message(message):
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text == "/start":
        send_welcome(chat_id)


def main():
    print(f"[{time.strftime('%H:%M:%S')}] @ie_srabot başlatılıyor...", flush=True)

    # Delete webhook
    result = send_request("deleteWebhook", {"drop_pending_updates": True})
    print(f"[{time.strftime('%H:%M:%S')}] Webhook silindi: {result}", flush=True)

    # Verify bot
    me = send_request("getMe")
    if me and me.get("ok"):
        print(f"[{time.strftime('%H:%M:%S')}] Bot: @{me['result']['username']} aktif!", flush=True)
    else:
        print(f"[{time.strftime('%H:%M:%S')}] Bot doğrulanamadı: {me}", flush=True)
        return

    offset = 0
    print(f"[{time.strftime('%H:%M:%S')}] Dinleniyor...", flush=True)
    error_count = 0

    while True:
        try:
            result = send_request("getUpdates", {
                "offset": offset,
                "timeout": 1,
                "allowed_updates": ["message", "callback_query"]
            })

            if result and result.get("ok"):
                error_count = 0
                for update in result.get("result", []):
                    offset = update["update_id"] + 1
                    if "message" in update:
                        handle_message(update["message"])
                    elif "callback_query" in update:
                        handle_callback(update["callback_query"])
            else:
                error_count += 1
                print(f"[{time.strftime('%H:%M:%S')}] getUpdates başarısız ({error_count}): {result}", flush=True)
                if error_count > 5:
                    time.sleep(10)

        except KeyboardInterrupt:
            print("Bot durduruluyor...", flush=True)
            break
        except Exception as e:
            error_count += 1
            print(f"[{time.strftime('%H:%M:%S')}] Hata ({error_count}): {e}", flush=True)
            time.sleep(5)


if __name__ == "__main__":
    main()
