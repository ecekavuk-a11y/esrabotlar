import requests
import json
import time

BOT_TOKEN = "8934662828:AAE0rzptqHmQFTZRcuKVDr0ET5892QVv_gc"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

ADMIN_USERNAME = "@malatya_esra44"

WELCOME_TEXT = """👋 Merhaba <b>Esra!</b> İE'sra VIP Kanalına hoş geldin 💎

━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ <b>VIP Kanalda Seni Neler Bekliyor?</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 Özel +18 içerikler
📸 Paylaşılmayan fotoğraf ve videolar
💬 Özel mesajlaşma imkânı
🎁 Sürpriz içerikler

━━━━━━━━━━━━━━━━━━━━━━━━━━
💳 <b>Üyelik Ücreti:</b> 1.500 ₺ / 30 gün
━━━━━━━━━━━━━━━━━━━━━━━━━━

Katılmak için aşağıdaki butona tıkla 👇"""

IBAN_TEXT = """💳 <b>Ödeme Bilgileri</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 <b>Banka Havalesi / EFT</b>
🏦 IBAN: <code>TR49 0082 9000 0949 1261 8500 57</code>
👤 Ad Soyad: <b>İsra SOĞUKPINAR</b>
💰 Tutar: <b>1.500 ₺</b>

━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 <b>Adımlar:</b>

1️⃣ Yukarıdaki IBAN'a <b>1.500 ₺</b> gönder
2️⃣ Ödeme ekran görüntüsünü bu sohbete gönder
3️⃣ Onay sonrası VIP kanal linki sana iletilir ✅

🕐 Onay süresi: Genellikle <b>birkaç dakika</b>

━━━━━━━━━━━━━━━━━━━━━━━━━━
❓ Sorularınız için: @malatya_esra44"""

PRICE_TEXT = """💰 <b>Fiyat & Süre</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 1 Aylık VIP Üyelik: <b>1.500 ₺</b>
📌 Stars ile Ödeme: <b>1.000 Stars</b>

⏰ Süre: 30 gün
🔄 Süre bitiminde yenileme yapılabilir

━━━━━━━━━━━━━━━━━━━━━━━━━━"""

HELP_TEXT = """❓ <b>Yardım</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 Ödeme yaptıktan sonra ekran görüntüsünü bu bota gönderin
📌 Onay sonrası VIP kanal linki iletilecektir
📌 Sorun yaşarsanız: @malatya_esra44

━━━━━━━━━━━━━━━━━━━━━━━━━━"""

PAYMENT_DONE_TEXT = """📸 <b>Ödeme ekran görüntüsünü gönder!</b>

Banka uygulamasından ödeme ekran görüntüsünü bu sohbete gönder.
Onaylandıktan sonra VIP kanal linki sana iletilecek ✅"""

session = requests.Session()


def send_request(method, data=None):
    for attempt in range(3):
        try:
            r = session.post(f"{API_URL}/{method}", json=data, timeout=15)
            return r.json()
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] Hata ({method}, deneme {attempt+1}): {e}", flush=True)
            time.sleep(2)
    return None


def get_main_keyboard():
    return {"inline_keyboard": [
        [
            {"text": "⭐ Stars ile Öde (1000)", "callback_data": "pay_stars"},
            {"text": "💳 IBAN ile Öde", "callback_data": "pay_iban"}
        ],
        [
            {"text": "💰 Fiyat & Süre", "callback_data": "price"},
            {"text": "❓ Yardım", "callback_data": "help"}
        ],
        [
            {"text": "🌐 Web Sitesi", "url": "https://www.malatyaesra.com"}
        ]
    ]}


def get_iban_keyboard():
    return {"inline_keyboard": [
        [{"text": "✅ Ödemeyi Yaptım", "callback_data": "payment_done"}],
        [{"text": "🔙 Ana Menü", "callback_data": "main_menu"}]
    ]}


def get_back_keyboard():
    return {"inline_keyboard": [
        [{"text": "🔙 Ana Menü", "callback_data": "main_menu"}]
    ]}


def send_welcome(chat_id):
    data = {
        "chat_id": chat_id,
        "text": WELCOME_TEXT,
        "parse_mode": "HTML",
        "reply_markup": get_main_keyboard()
    }
    result = send_request("sendMessage", data)
    if result and result.get("ok"):
        print(f"[{time.strftime('%H:%M:%S')}] Hoş geldin: {chat_id}", flush=True)


def handle_callback(callback_query):
    chat_id = callback_query["message"]["chat"]["id"]
    message_id = callback_query["message"]["message_id"]
    callback_id = callback_query["id"]
    data = callback_query.get("data", "")

    send_request("answerCallbackQuery", {"callback_query_id": callback_id})

    if data == "pay_iban":
        send_request("sendMessage", {
            "chat_id": chat_id,
            "text": IBAN_TEXT,
            "parse_mode": "HTML",
            "reply_markup": get_iban_keyboard()
        })

    elif data == "pay_stars":
        send_request("sendInvoice", {
            "chat_id": chat_id,
            "title": "VIP Üyelik - 30 Gün",
            "description": "İE'sra VIP Kanalına 30 günlük erişim",
            "payload": "vip_30_days",
            "currency": "XTR",
            "prices": [{"label": "VIP Üyelik", "amount": 1000}]
        })

    elif data == "price":
        send_request("sendMessage", {
            "chat_id": chat_id,
            "text": PRICE_TEXT,
            "parse_mode": "HTML",
            "reply_markup": get_back_keyboard()
        })

    elif data == "help":
        send_request("sendMessage", {
            "chat_id": chat_id,
            "text": HELP_TEXT,
            "parse_mode": "HTML",
            "reply_markup": get_back_keyboard()
        })

    elif data == "payment_done":
        send_request("sendMessage", {
            "chat_id": chat_id,
            "text": PAYMENT_DONE_TEXT,
            "parse_mode": "HTML"
        })

    elif data == "main_menu":
        send_request("sendMessage", {
            "chat_id": chat_id,
            "text": WELCOME_TEXT,
            "parse_mode": "HTML",
            "reply_markup": get_main_keyboard()
        })


def handle_message(message):
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text == "/start":
        send_welcome(chat_id)
    elif message.get("photo") or message.get("document"):
        # User sent a photo (payment screenshot)
        user = message.get("from", {})
        username = user.get("username", "")
        first_name = user.get("first_name", "")
        user_id = user.get("id", "")
        
        send_request("sendMessage", {
            "chat_id": chat_id,
            "text": "✅ Ödeme ekran görüntünüz alındı!\n\n⏳ En kısa sürede kontrol edilecek ve VIP kanal linki iletilecektir.\n\n❓ Sorularınız için: @malatya_esra44",
            "parse_mode": "HTML"
        })
        print(f"[{time.strftime('%H:%M:%S')}] 📸 Ödeme SS geldi: {first_name} (@{username}) ID:{user_id}", flush=True)


def handle_pre_checkout(pre_checkout_query):
    send_request("answerPreCheckoutQuery", {
        "pre_checkout_query_id": pre_checkout_query["id"],
        "ok": True
    })


def handle_successful_payment(message):
    chat_id = message["chat"]["id"]
    user = message.get("from", {})
    print(f"[{time.strftime('%H:%M:%S')}] ⭐ Stars ödeme başarılı: {user.get('first_name', '')} ID:{user.get('id', '')}", flush=True)
    send_request("sendMessage", {
        "chat_id": chat_id,
        "text": "✅ Ödemeniz başarıyla alındı!\n\n⏳ VIP kanal linki en kısa sürede iletilecektir.\n\n❓ Sorularınız için: @malatya_esra44",
        "parse_mode": "HTML"
    })


def main():
    print(f"[{time.strftime('%H:%M:%S')}] @Vip_iesrabot başlatılıyor...", flush=True)

    send_request("deleteWebhook", {"drop_pending_updates": True})

    me = send_request("getMe")
    if me and me.get("ok"):
        print(f"[{time.strftime('%H:%M:%S')}] Bot: @{me['result']['username']} aktif!", flush=True)
    else:
        print(f"[{time.strftime('%H:%M:%S')}] Bot doğrulanamadı: {me}", flush=True)
        return

    offset = 0
    print(f"[{time.strftime('%H:%M:%S')}] Dinleniyor...", flush=True)

    while True:
        try:
            result = send_request("getUpdates", {
                "offset": offset,
                "timeout": 1,
                "allowed_updates": ["message", "callback_query", "pre_checkout_query"]
            })

            if result and result.get("ok"):
                for update in result.get("result", []):
                    offset = update["update_id"] + 1

                    if "message" in update:
                        msg = update["message"]
                        if msg.get("successful_payment"):
                            handle_successful_payment(msg)
                        else:
                            handle_message(msg)
                    elif "callback_query" in update:
                        handle_callback(update["callback_query"])
                    elif "pre_checkout_query" in update:
                        handle_pre_checkout(update["pre_checkout_query"])

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] Hata: {e}", flush=True)
            time.sleep(3)


if __name__ == "__main__":
    main()
