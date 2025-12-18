# 🎬 Telegram Video Downloader Bot

YouTube, Instagram, TikTok, Facebook va boshqa 1000+ platformalardan watermarksiz video yuklovchi Telegram bot.

## ⚠️ MUHIM OGOHLANTIRISH

**Bu bot faqat OMMAVIY va RUXSAT ETILGAN kontentni yuklab olish uchun mo'ljallangan.**

### Qonuniy Javobgarlik:
- ❌ Mualliflik huquqlari bilan himoyalangan kontentni yuklab olish **QONUNGA ZID**
- ❌ Shaxsiy yoki maxfiy ma'lumotlarni yuklab olish **QONUNGA ZID**
- ✅ Foydalanuvchi o'z javobgarligida kontentni yuklab oladi
- ✅ Bot egasi yuklangan kontentlar uchun javobgar **EMAS**

### Qabul qiling:
Bu botni ishlatish orqali siz quyidagiga rozilik bildirasiz:
1. Faqat ommaviy va ruxsat etilgan kontentni yuklab olasiz
2. Mualliflik huquqlarini hurmat qilasiz
3. Bot egasi yuklangan kontentlar uchun javobgar emas

## ✨ Xususiyatlar

- 📹 **Ko'p platformali qo'llab-quvvatlash**: YouTube, Instagram, TikTok, Facebook, Twitter va boshqalar
- 🎯 **Sifat tanlash**: 360p, 480p, 720p, 1080p yoki eng yaxshi sifat
- 🎵 **MP3 konvertatsiya**: Videolarni MP3 audio formatga o'tkazish
- 🚫 **Watermarksiz**: Barcha videolar watermarksiz yuklanadi
- ⚡ **Tez va oson**: Faqat linkni yuboring va formatni tanlang

## 📋 Talablar

- Python 3.8 yoki yuqori
- FFmpeg (audio konvertatsiya uchun)

## 🚀 O'rnatish

### 1. Repository ni klonlash

```bash
git clone <repository-url>
cd bot
```

### 2. Virtual muhit yaratish (ixtiyoriy, lekin tavsiya etiladi)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Kerakli kutubxonalarni o'rnatish

```bash
pip install -r requirements.txt
```

### 4. FFmpeg o'rnatish

#### Windows:
1. [FFmpeg rasmiy saytidan](https://ffmpeg.org/download.html) yuklab oling
2. ZIP faylni ochib, `bin` papkasini PATH ga qo'shing

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install ffmpeg
```

#### macOS:
```bash
brew install ffmpeg
```

### 5. Bot tokenini sozlash

1. Telegram da [@BotFather](https://t.me/BotFather) ga o'ting
2. `/newbot` komandasini yuboring va ko'rsatmalarga amal qiling
3. Olingan tokenni nusxalang
4. `.env.example` faylini `.env` ga o'zgartiring:
   ```bash
   # Windows
   copy .env.example .env
   
   # Linux/Mac
   cp .env.example .env
   ```
5. `.env` faylini oching va tokenni kiriting:
   ```
   BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

## 🎮 Ishga tushirish

```bash
python bot.py
```

Bot ishga tushgach, Telegram da botingizni toping va `/start` komandasini yuboring.

## 📱 Foydalanish

1. **Botni boshlash**: `/start` komandasini yuboring
2. **Video linkini yuborish**: Istalgan qo'llab-quvvatlanadigan platformadan video linkini yuboring
3. **Format tanlash**: 
   - Video sifatini tanlang (360p, 480p, 720p, 1080p, Best)
   - Yoki MP3 audio formatni tanlang
4. **Yuklab olish**: Bot video/audio ni yuklab, sizga yuboradi

## 🌐 Qo'llab-quvvatlanadigan platformalar

- ✅ YouTube (youtube.com, youtu.be)
- ✅ Instagram (instagram.com)
- ✅ TikTok (tiktok.com)
- ✅ Facebook (facebook.com)
- ✅ Twitter/X (twitter.com, x.com)
- ✅ Reddit (reddit.com)
- ✅ Vimeo (vimeo.com)
- ✅ Dailymotion (dailymotion.com)
- ✅ Va 1000+ boshqa platformalar

To'liq ro'yxat uchun [yt-dlp qo'llab-quvvatlanadigan saytlar](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md) sahifasiga qarang.

## ⚙️ Sozlamalar

### Fayl hajmi limiti

Telegram Bot API orqali maksimal 50MB gacha fayllar yuborilishi mumkin. Agar video hajmi kattaroq bo'lsa, pastroq sifatni tanlang.

### Yuklab olingan fayllar

Barcha yuklab olingan fayllar `downloads/` papkasida vaqtinchalik saqlanadi va yuborilgandan keyin avtomatik o'chiriladi.

## 🛠️ Texnologiyalar

- **python-telegram-bot**: Telegram Bot API bilan ishlash
- **yt-dlp**: Video yuklab olish (youtube-dl ning yaxshilangan versiyasi)
- **FFmpeg**: Audio/video konvertatsiya

## 📝 Komandalar

- `/start` - Botni ishga tushirish va xush kelibsiz xabarini ko'rish
- `/help` - Yordam va qo'llanma

## ⚠️ Muhim eslatmalar

1. Bot faqat ommaviy videolarni yuklay oladi
2. Mualliflik huquqi bilan himoyalangan kontentni yuklab olishda ehtiyot bo'ling
3. Ba'zi platformalar yuklab olishni cheklashi mumkin
4. Katta hajmli videolar uchun vaqt talab qilinishi mumkin

## 🐛 Muammolarni hal qilish

### "FFmpeg topilmadi" xatosi
FFmpeg o'rnatilganligiga va PATH ga qo'shilganligiga ishonch hosil qiling.

### "Fayl hajmi juda katta" xatosi
Pastroq sifatni tanlang yoki MP3 formatni sinab ko'ring.

### "Video ma'lumotlarini olishda xatolik"
- Linkni tekshiring
- Videoning ommaviy ekanligiga ishonch hosil qiling
- Internetga ulanishni tekshiring

## 🌐 Hosting (24/7 Ishlash)

### Muammo:
Agar bot kompyuterda ishlatilsa, terminal yopilganda bot to'xtaydi.

### Yechim - Cloud Hosting:

#### Bepul Variantlar:
- **Render.com** - Bepul, 15 daqiqa faolsizlikdan keyin uxlaydi
- **Railway.app** - Bepul, oyiga 500 soat
- **PythonAnywhere** - Bepul, cheklangan

#### Pullik Variantlar (Tavsiya etiladi):
- **Digital Ocean** - $5/oy
- **Vultr** - $3.5/oy
- **Linode** - $5/oy
- **AWS** - $1-5/oy (free tier)

#### Render.com ga Deploy:
```bash
1. render.com ga kiriting
2. GitHub repo ulang
3. Bot fayllarini yuklang
4. Deploy qiling
5. 24/7 ishlab turadi!
```

## 💰 Pul Ishlash

### 1. Premium Subscription
```
Bepul: 3 ta video/kun
Premium: Cheksiz video
Narxi: $2-5/oy
```

### 2. Reklama
```
Bot xabarida reklama
Narxi: $100-500/oy
```

### 3. Affiliate
```
YouTube Premium, Spotify, Netflix
Narxi: 5-30% komissiya
```

### 4. Donation
```
/donate komandasi
Narxi: Ixtiyoriy
```

### 5. API Service
```
Boshqa botlar uchun API
Narxi: $50-500/oy
```

## 📄 Litsenziya

Ushbu loyiha shaxsiy va ta'lim maqsadlari uchun yaratilgan.

## 🤝 Hissa qo'shish

Xatoliklarni topganingizda yoki yangi funksiyalar qo'shmoqchi bo'lsangiz, issue yarating yoki pull request yuboring.

## 📧 Aloqa

Savollar yoki takliflar bo'lsa, issue yaratishingiz mumkin.

---

**Eslatma**: Ushbu botdan foydalanishda mualliflik huquqlarini hurmat qiling va faqat ruxsat etilgan kontentni yuklab oling.
# telegram-video-bot
