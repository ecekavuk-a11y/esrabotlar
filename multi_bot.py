#!/usr/bin/env python3
"""
Telegram Multi-Bot - Otomatik Onay + Çoklu Tepki + Hoş Geldin + İstatistik
"""

import time
import requests
import json
import random
import threading
from datetime import datetime, timedelta

PRIMARY_TOKEN = "8641372083:AAETQNKwlxcvwmp1ukWFqj3n0WstifK4lNI"

BOTS = [
    {
        "token": "8641372083:AAETQNKwlxcvwmp1ukWFqj3n0WstifK4lNI",
        "name": "bellyuasbot",
        "emojis": ["🔥", "😍", "💋", "❤️", "👏"],
    },
    {
        "token": "8751638714:AAEfXNI8PS2fXdOHo9QOGNhMUps_-9TXXKM",
        "name": "isra_melegi_bot",
        "emojis": ["❤️‍🔥", "💯", "⚡", "👀", "🎉"],
    },
    {
        "token": "8795381995:AAHAjOCAbWfw81whBtsq4qPiBO2HC-2yH7Q",
        "name": "Sesunun_bot",
        "emojis": ["🎉", "👏", "😈", "💅", "🔥"],
    },
    {
        "token": "8332061202:AAEFLuJp5KPs71YdbRIl5CcqI9eQv_2KprA",
        "name": "Bellyasbot",
        "emojis": ["👀", "😈", "💋", "❤️", "😍"],
    },
    {
        "token": "8649828266:AAGiN_K6nDiIBMzHmrCk-CYzBVNbK_QULwM",
        "name": "Zelusumun_bot",
        "emojis": ["🔥", "😍", "❤️‍🔥", "💯", "👏"],
    },
    {
        "token": "8423804850:AAEsIBrxOPOZ8cuICwLamcBTSjllvUeZlgE",
        "name": "Zelisahin_bot",
        "emojis": ["❤️", "💅", "😘", "🎉", "⚡"],
    },
    {
        "token": "8538659088:AAFHIb44BLGpZY8F2-tJkglgjSyMdOWI_zA",
        "name": "Qubranin_bot",
        "emojis": ["💋", "😘", "👀", "🔥", "😈"],
    },
    {
        "token": "8645202362:AAHlQ3l29IDAT0EP42iEiAS2NxiOm8xkP8k",
        "name": "Qubeaninin_bot",
        "emojis": ["❤️‍🔥", "❤️", "💋", "👏", "😍"],
    },
]

CHAT_IDS = [
    -1003494573579,   # Malatya Esra Bal (İÇERİKLER)
    -1003524644687,   # Onlineİsra
    -1002956424495,   # MALATYA ESRA BAL
]

# Hoş geldin mesajı
WELCOME_MESSAGE = """Hoş geldin aşk 🥰
Seni burada görmek güzel 😍
Belki istediğin şeyler var.
Günün her anı seni avlayacağım 😈
İyi izle... 💋"""

# Bot sahibinin chat ID'si (istatistik göndermek için)
OWNER_CHAT_ID = None  # Otomatik algılanacak

# İstatistikler
stats = {
    "approved": 0,
    "reactions": 0,
    "new_members": 0,
    "posts": 0,
    "daily_approved": 0,
    "daily_reactions": 0,
    "daily_new_members": 0,
    "daily_posts": 0,
    "last_reset": datetime.now().strftime("%Y-%m-%d"),
    "channels": {},  # kanal bazlı istatistik
}

def log(msg):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {msg}", flush=True)

def api_call(token, method, params=None, max_retries=3):
    url = f"https://api.telegram.org/bot{token}/{method}"
    for attempt in range(max_retries):
        try:
            resp = requests.post(url, json=params or {}, timeout=60)
            return resp.json()
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 * (attempt + 1))
    return None

def reset_daily_stats():
    """Günlük istatistikleri sıfırla"""
    today = datetime.now().strftime("%Y-%m-%d")
    if stats["last_reset"] != today:
        stats["daily_approved"] = 0
        stats["daily_reactions"] = 0
        stats["daily_new_members"] = 0
        stats["daily_posts"] = 0
        stats["last_reset"] = today

def get_channel_stats(chat_id, chat_title):
    """Kanal bazlı istatistik al"""
    if chat_id not in stats["channels"]:
        stats["channels"][chat_id] = {
            "title": chat_title,
            "members_joined": 0,
            "posts": 0,
            "reactions": 0,
        }
    return stats["channels"][chat_id]

def send_welcome_message(token, user_id, first_name):
    """Yeni üyeye hoş geldin mesajı gönder"""
    try:
        result = api_call(token, "sendMessage", {
            "chat_id": user_id,
            "text": WELCOME_MESSAGE,
            "parse_mode": "HTML"
        })
        if result and result.get("ok"):
            log(f"💌 Hoş geldin mesajı gönderildi: {first_name}")
        else:
            error = result.get("description", "?") if result else "Yanıt yok"
            log(f"✗ Hoş geldin gönderilemedi ({first_name}): {error}")
    except Exception as e:
        log(f"✗ Hoş geldin hatası: {e}")

def add_reaction_with_bot(bot, chat_id, message_id):
    """Belirli bir bot ile tepki ekle"""
    emoji = random.choice(bot["emojis"])
    result = api_call(bot["token"], "setMessageReaction", {
        "chat_id": chat_id,
        "message_id": message_id,
        "reaction": [{"type": "emoji", "emoji": emoji}],
        "is_big": True
    })
    if result and result.get("ok"):
        stats["reactions"] += 1
        stats["daily_reactions"] += 1
        log(f"🎯 @{bot['name']}: {emoji} ekledi (Toplam: {stats['reactions']})")
    else:
        error = result.get("description", "?") if result else "Yanıt yok"
        log(f"✗ @{bot['name']}: tepki eklenemedi - {error}")

def handle_join_request(token, update):
    """Katılım isteğini onayla + hoş geldin mesajı gönder"""
    join_req = update.get("chat_join_request", {})
    chat = join_req.get("chat", {})
    user = join_req.get("from", join_req.get("user", {}))
    
    chat_id = chat.get("id")
    chat_title = chat.get("title", "?")
    user_id = user.get("id")
    first_name = user.get("first_name", "")
    last_name = user.get("last_name", "")
    user_name = f"{first_name} {last_name}".strip() or str(user_id)
    
    if not chat_id or not user_id:
        return
    
    # Katılım isteğini onayla
    result = api_call(token, "approveChatJoinRequest", {
        "chat_id": chat_id,
        "user_id": user_id
    })
    
    if result and result.get("ok"):
        stats["approved"] += 1
        stats["daily_approved"] += 1
        stats["daily_new_members"] += 1
        stats["new_members"] += 1
        
        ch = get_channel_stats(chat_id, chat_title)
        ch["members_joined"] += 1
        
        log(f"✓ ONAYLANDI: {user_name} -> {chat_title} (Toplam: {stats['approved']})")
        
        # Hoş geldin mesajı gönder (özel mesaj olarak)
        send_welcome_message(token, user_id, first_name)
    else:
        error = result.get("description", "?") if result else "Yanıt yok"
        log(f"✗ Onay başarısız: {user_name} -> {chat_title} - {error}")

def handle_channel_post(update):
    """Kanal gönderisine TÜM botlarla tepki ekle"""
    post = update.get("channel_post", {})
    chat = post.get("chat", {})
    chat_id = chat.get("id")
    message_id = post.get("message_id")
    chat_title = chat.get("title", "?")
    
    if not chat_id or not message_id:
        return
    
    stats["posts"] += 1
    stats["daily_posts"] += 1
    
    ch = get_channel_stats(chat_id, chat_title)
    ch["posts"] += 1
    
    log(f"📨 Yeni gönderi: {chat_title} (msg: {message_id})")
    
    # Her bot farklı emoji eklesin
    for i, bot in enumerate(BOTS):
        time.sleep(0.5)
        add_reaction_with_bot(bot, chat_id, message_id)

def handle_private_message(token, update):
    """Özel mesajları işle - /stats komutu için"""
    global OWNER_CHAT_ID
    msg = update.get("message", {})
    chat = msg.get("chat", {})
    text = msg.get("text", "")
    chat_id = chat.get("id")
    
    if not chat_id or chat.get("type") != "private":
        return
    
    # İlk mesaj gönderen kişiyi sahip olarak kaydet
    if OWNER_CHAT_ID is None:
        OWNER_CHAT_ID = chat_id
        log(f"👤 Sahip algılandı: {chat_id}")
    
    if text.startswith("/start"):
        api_call(token, "sendMessage", {
            "chat_id": chat_id,
            "text": "🤖 Bot aktif!\n\n📊 İstatistikleri görmek için /stats yazın\n📈 Günlük rapor için /gunluk yazın"
        })
    
    elif text.startswith("/stats"):
        reset_daily_stats()
        stats_text = f"""📊 GENEL İSTATİSTİKLER

✅ Toplam Onaylanan: {stats['approved']}
👥 Toplam Yeni Üye: {stats['new_members']}
🎯 Toplam Tepki: {stats['reactions']}
📨 Toplam Gönderi: {stats['posts']}

📅 BUGÜNKÜ İSTATİSTİKLER ({stats['last_reset']})

✅ Bugün Onaylanan: {stats['daily_approved']}
👥 Bugün Yeni Üye: {stats['daily_new_members']}
🎯 Bugün Tepki: {stats['daily_reactions']}
📨 Bugün Gönderi: {stats['daily_posts']}"""

        # Kanal bazlı istatistik
        if stats["channels"]:
            stats_text += "\n\n📢 KANAL BAZLI:"
            for cid, ch in stats["channels"].items():
                stats_text += f"\n\n🔹 {ch['title']}"
                stats_text += f"\n   👥 Üye: +{ch['members_joined']}"
                stats_text += f"\n   📨 Gönderi: {ch['posts']}"
                stats_text += f"\n   🎯 Tepki: {ch['reactions']}"
        
        api_call(token, "sendMessage", {
            "chat_id": chat_id,
            "text": stats_text
        })
        log(f"📊 İstatistik gönderildi: {chat_id}")
    
    elif text.startswith("/gunluk") or text.startswith("/günlük"):
        reset_daily_stats()
        daily_text = f"""📈 GÜNLÜK RAPOR - {stats['last_reset']}

✅ Onaylanan: {stats['daily_approved']}
👥 Yeni Üye: {stats['daily_new_members']}
🎯 Tepki: {stats['daily_reactions']}
📨 Gönderi: {stats['daily_posts']}

🤖 Bot çalışma durumu: Aktif ✓
🔄 8 bot tepki sistemi: Aktif ✓"""
        
        api_call(token, "sendMessage", {
            "chat_id": chat_id,
            "text": daily_text
        })

def main():
    log("=" * 50)
    log("Telegram Multi-Bot v3")
    log("Onay + Tepki + Hoş Geldin + İstatistik")
    log("=" * 50)
    log(f"Bot sayısı: {len(BOTS)}")
    log(f"Kanal sayısı: {len(CHAT_IDS)}")
    log("")
    
    primary_bot = BOTS[0]
    token = primary_bot["token"]
    
    log("Botlar başlatılıyor...")
    
    # Tüm botların webhook'unu sil
    for bot in BOTS:
        api_call(bot["token"], "deleteWebhook", {"drop_pending_updates": False})
        me = api_call(bot["token"], "getMe")
        if me and me.get("ok"):
            log(f"  @{me['result']['username']} hazır ✓")
        else:
            log(f"  @{bot['name']} doğrulanamadı ✗")
    
    log("")
    log("Tüm botlar aktif! Dinleniyor...")
    log(f"Hoş geldin mesajı: Aktif ✓")
    log(f"İstatistik: /stats veya /gunluk komutu ile")
    log("")
    
    # Birincil bot polling
    api_call(token, "deleteWebhook", {"drop_pending_updates": False})
    time.sleep(1)
    
    me = api_call(token, "getMe")
    if not me or not me.get("ok"):
        log("Birincil bot doğrulanamadı!")
        return
    log(f"@{me['result']['username']} aktif!")
    
    offset = 0
    
    while True:
        try:
            reset_daily_stats()
            
            result = api_call(token, "getUpdates", {
                "offset": offset,
                "limit": 100,
                "timeout": 30,
                "allowed_updates": ["chat_join_request", "channel_post", "message"]
            })
            
            if not result or not result.get("ok"):
                time.sleep(5)
                continue
            
            for update in result.get("result", []):
                update_id = update.get("update_id", 0)
                offset = update_id + 1
                
                if "chat_join_request" in update:
                    handle_join_request(token, update)
                
                if "channel_post" in update:
                    handle_channel_post(update)
                
                if "message" in update:
                    handle_private_message(token, update)
                    
        except Exception as e:
            log(f"Hata: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
