# Telegram Botları - 7/24 Ücretsiz Hosting Kurulumu

## Bu paket ne içeriyor?

- **multi_bot.py** - 8 bot ile emoji tepki + katılım onayı + hoş geldin mesajı + istatistik
- **ie_srabot.py** - @ie_srabot zorunlu katılım botu (4 kanala yönlendirme)
- **vip_iesrabot.py** - @Vip_iesrabot VIP satış botu (IBAN + Stars ödeme)
- **main.py** - Tüm botları tek seferde başlatan ana script

## Render.com'a Deploy (ÜCRETSİZ - 7/24 Çalışır)

### Adım 1: GitHub Hesabı Oluştur (varsa atla)
1. https://github.com adresine git
2. "Sign Up" tıkla ve hesap oluştur

### Adım 2: GitHub'a Dosyaları Yükle
1. https://github.com/new adresine git
2. Repository name: `telegram-bots` yaz
3. "Create repository" tıkla
4. "uploading an existing file" linkine tıkla
5. Bu klasördeki TÜM dosyaları sürükle-bırak ile yükle
6. "Commit changes" tıkla

### Adım 3: Render.com'a Deploy Et
1. https://render.com adresine git
2. GitHub hesabınla giriş yap
3. "New +" butonuna tıkla
4. "Background Worker" seç
5. GitHub reponuzu bağla (telegram-bots)
6. Ayarlar:
   - Name: telegram-bots
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python -u main.py`
   - Plan: **Free**
7. "Create Background Worker" tıkla

### Bitti! 🎉
Bot artık 7/24 çalışacak. Render.com ücretsiz planda aylık 750 saat veriyor (tam ay yeterli).

## Alternatif: Railway.app

1. https://railway.app adresine git
2. GitHub ile giriş yap
3. "New Project" > "Deploy from GitHub Repo"
4. telegram-bots reposunu seç
5. Otomatik deploy edilecek

## Notlar

- Token'ları değiştirmek isterseniz ilgili .py dosyasını düzenleyin
- Render.com'da bot duruyorsa Dashboard'dan "Manual Deploy" yapın
- Sorun olursa Render.com loglarını kontrol edin
