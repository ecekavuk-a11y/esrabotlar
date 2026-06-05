#!/usr/bin/env python3
"""
Tüm Telegram Botları - Tek Script
1. Multi-Bot: Emoji tepki + Katılım onayı + Hoş geldin + İstatistik
2. İE'sra Bot: Zorunlu katılım botu
3. VIP Bot: VIP satış botu
"""

import threading
import time
import sys
import os

# Bot scriptlerini import et
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_multi_bot():
    """Multi emoji + onay botu"""
    import multi_bot
    multi_bot.main()

def run_ie_srabot():
    """Zorunlu katılım botu"""
    import ie_srabot
    ie_srabot.main()

def run_vip_bot():
    """VIP satış botu"""
    import vip_iesrabot
    vip_iesrabot.main()

if __name__ == "__main__":
    print("=" * 50, flush=True)
    print("TÜM BOTLAR BAŞLATILIYOR...", flush=True)
    print("=" * 50, flush=True)
    
    threads = [
        threading.Thread(target=run_multi_bot, name="MultiBot", daemon=True),
        threading.Thread(target=run_ie_srabot, name="IeSraBot", daemon=True),
        threading.Thread(target=run_vip_bot, name="VipBot", daemon=True),
    ]
    
    for t in threads:
        t.start()
        print(f"[+] {t.name} başlatıldı", flush=True)
        time.sleep(2)
    
    print("", flush=True)
    print("Tüm botlar çalışıyor! Ctrl+C ile durdurun.", flush=True)
    
    try:
        while True:
            time.sleep(60)
            # Thread health check
            for t in threads:
                if not t.is_alive():
                    print(f"[!] {t.name} durdu, yeniden başlatılıyor...", flush=True)
    except KeyboardInterrupt:
        print("\nBotlar durduruluyor...", flush=True)
