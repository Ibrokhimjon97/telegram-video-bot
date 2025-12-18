import os
import logging
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import yt_dlp
import asyncio

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot tokenini olish
BOT_TOKEN = os.getenv('BOT_TOKEN', '8313903030:AAGw8pOABWDHlWVyy-1oaWCwSuVfdu7kqOU')

# Yuklab olingan fayllar uchun papka
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)


def is_valid_url(url: str) -> bool:
    """URL'ni tekshirish"""
    url_pattern = re.compile(
        r'^https?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None


def is_playlist_url(url: str) -> bool:
    """Playlist URL'ni tekshirish"""
    playlist_keywords = ['playlist', 'list=', 'channel/', 'watch?v=.*list=']
    return any(keyword in url.lower() for keyword in playlist_keywords)


def get_video_info(url: str) -> dict:
    """Video haqida ma'lumot olish"""
    ydl_opts = {
        'quiet': False,
        'no_warnings': False,
        'extract_flat': False,
        'socket_timeout': 30,
        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'android', 'mweb'],
                'skip': ['hls', 'dash', 'translated_subs']
            },
            'instagram': {
                'skip_login': False
            }
        },
        'geo_bypass': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Sec-Fetch-Mode': 'navigate',
        },
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                'title': info.get('title', 'Unknown'),
                'duration': info.get('duration', 0),
                'formats': info.get('formats', []),
                'thumbnail': info.get('thumbnail', ''),
            }
    except Exception as e:
        logger.error(f"Video ma'lumotlarini olishda xato: {str(e)}")
        logger.error(f"URL: {url}")
        logger.error(f"Exception type: {type(e).__name__}")
        return None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start komandasi"""
    welcome_message = (
        "🎬 <b>Video Downloader Bot</b>\n\n"
        "Salom! Men sizga quyidagi platformalardan videolarni yuklab beraman:\n"
        "✅ YouTube\n"
        "✅ Instagram\n"
        "✅ TikTok\n"
        "✅ Facebook\n"
        "✅ Twitter\n"
        "✅ Va boshqa ko'plab platformalar\n\n"
        "📝 <b>Qanday foydalanish:</b>\n"
        "1. Video linkini yuboring\n"
        "2. Sifat va formatni tanlang (Video yoki MP3)\n"
        "3. Yuklab olishni kuting!\n\n"
        "⚠️ <b>MUHIM OGOHLANTIRISH:</b>\n"
        "Bu bot faqat OMMAVIY va RUXSAT ETILGAN kontentni yuklab olish uchun.\n"
        "Mualliflik huquqlari bilan himoyalangan kontentni yuklab olish QONUNGA ZID.\n"
        "Siz o'z javobgarligida kontentni yuklab olasiz.\n\n"
        "💡 Maslahat: Linkni to'g'ri nusxalang!\n"
        "/help - Batafsil yordam"
    )
    await update.message.reply_text(welcome_message, parse_mode='HTML')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help komandasi"""
    help_text = (
        "📚 <b>Yordam</b>\n\n"
        "<b>Qo'llab-quvvatlanadigan platformalar:</b>\n"
        "• YouTube (youtube.com, youtu.be)\n"
        "• Instagram (instagram.com)\n"
        "• TikTok (tiktok.com)\n"
        "• Facebook (facebook.com)\n"
        "• Twitter (twitter.com, x.com)\n"
        "• Va 1000+ boshqa saytlar\n\n"
        "<b>Format tanlash:</b>\n"
        "• 📹 Video - turli sifatlarda (360p, 480p, 720p, 1080p)\n"
        "• 🎵 MP3 - faqat audio fayl\n"
        "• 🔗 Direct Link - Katta fayllar uchun (1 GB, 2 GB, 5 GB+)\n\n"
        "<b>⚠️ Muhim ma'lumot:</b>\n"
        "• Telegram orqali yuborish limiti: 50 MB\n"
        "• Katta videolar uchun Direct Link foydalaning\n"
        "• Direct Link - hajm cheklovi yo'q!\n\n"
        "<b>Komandalar:</b>\n"
        "/start - Botni ishga tushirish\n"
        "/help - Yordam\n"
    )
    await update.message.reply_text(help_text, parse_mode='HTML')


async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """URL'ni qayta ishlash"""
    url = update.message.text.strip()
    
    if not is_valid_url(url):
        await update.message.reply_text(
            "❌ Noto'g'ri URL! Iltimos, to'g'ri video linkini yuboring.\n"
            "Qo'llab-quvvatlanuvchi platformalar: YouTube, TikTok, Instagram, Facebook, Twitter va boshqalar."
        )
        return
    
    # Playlist tekshirish
    if is_playlist_url(url):
        await update.message.reply_text(
            "⚠️ **OGOHLANTIRISH!**\n\n"
            "Siz **Playlist** linki yubordingiz!\n\n"
            "Playlist'dan **339 ta video** yuklab olmoqchi bo'lmoqdasiz.\n"
            "Bu juda ko'p vaqt oladi va server'ni yuklab qo'yadi.\n\n"
            "❌ Iltimos, **alohida video** linkini yuboring:\n"
            "✅ https://youtu.be/VIDEO_ID\n"
            "✅ https://www.tiktok.com/@user/video/123456\n"
            "✅ https://www.facebook.com/video/123456"
        )
        return
    
    # Yuklanish jarayonini boshlash
    processing_msg = await update.message.reply_text("⏳ Video ma'lumotlari yuklanmoqda...")
    
    try:
        # Video haqida ma'lumot olish
        video_info = get_video_info(url)
        
        if not video_info:
            await processing_msg.edit_text(
                "❌ Video ma'lumotlarini olishda xatolik yuz berdi.\n\n"
                "🔍 Tekshiring:\n"
                "• Linkni to'g'ri nusxaladingizmi?\n"
                "• Video hali mavjudmi?\n"
                "• Internet ulanishingiz yaxshimi?\n\n"
                "💡 Boshqa linkni yuboring yoki /help buyrug'ini ishlating."
            )
            return
        
        # Kontekstga saqlash
        context.user_data['video_url'] = url
        context.user_data['video_info'] = video_info
        
        # Video hajmini tekshirish
        estimated_size_mb = 0
        formats = video_info.get('formats', [])
        
        # Eng yaxshi sifatdagi video hajmini topish
        for fmt in formats:
            if fmt.get('filesize') and fmt.get('height', 0) >= 720:
                size_mb = fmt['filesize'] / (1024 * 1024)
                if size_mb > estimated_size_mb:
                    estimated_size_mb = size_mb
        
        # Agar hajm aniqlanmagan bo'lsa, taxminiy hisoblash (davomiylik asosida)
        if estimated_size_mb == 0 and video_info['duration'] > 0:
            # Taxminiy: 1 daqiqa HD video ≈ 10-15 MB
            estimated_size_mb = (video_info['duration'] / 60) * 12
        
        # Sifat tanlash tugmalarini yaratish
        keyboard = [
            [
                InlineKeyboardButton("🎬 1080p Video", callback_data="quality_1080p"),
                InlineKeyboardButton("🎬 720p Video", callback_data="quality_720p"),
            ],
            [
                InlineKeyboardButton("🎬 480p Video", callback_data="quality_480p"),
                InlineKeyboardButton("🎬 360p Video", callback_data="quality_360p"),
            ],
            [
                InlineKeyboardButton("🎬 Best Quality", callback_data="quality_best"),
            ],
            [
                InlineKeyboardButton("🎵 MP3 Audio", callback_data="format_mp3"),
            ],
            [
                InlineKeyboardButton("🔗 Get Direct Link (Katta fayllar uchun)", callback_data="get_direct_link"),
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        title = video_info['title'][:50] + "..." if len(video_info['title']) > 50 else video_info['title']
        
        # Xabar tayyorlash
        message = f"✅ <b>Video topildi!</b>\n\n"
        message += f"📝 <b>Nomi:</b> {title}\n"
        message += f"⏱ <b>Davomiyligi:</b> {video_info['duration'] // 60}:{video_info['duration'] % 60:02d}\n"
        
        # Hajm haqida ogohlantirish
        if estimated_size_mb > 50:
            message += f"📦 <b>Taxminiy hajm:</b> ~{estimated_size_mb:.0f} MB\n\n"
            message += "⚠️ <b>MUHIM OGOHLANTIRISH!</b>\n"
            message += f"Bu video juda katta ({estimated_size_mb:.0f} MB)\n"
            message += "Telegram orqali yuborish limiti: 50 MB\n\n"
            message += "💡 <b>Tavsiyalar:</b>\n"
            message += "1️⃣ <b>Pastroq sifatni tanlang</b> (480p, 360p)\n"
            message += "2️⃣ <b>MP3 formatni tanlang</b> (faqat audio)\n"
            message += "3️⃣ <b>🔗 Get Direct Link</b> - To'g'ridan-to'g'ri yuklab oling\n"
            message += "   (1 GB, 2 GB, 5 GB - istalgan hajm!)\n\n"
            message += "🔗 <b>Direct Link nima?</b>\n"
            message += "• Bot sizga yuklab olish linkini beradi\n"
            message += "• Linkni brauzerda ochib, videoni yuklab olasiz\n"
            message += "• Hajm cheklovi yo'q!\n"
            message += "• Telegram orqali emas, to'g'ridan-to'g'ri serverdan\n\n"
        elif estimated_size_mb > 30:
            message += f"📦 <b>Taxminiy hajm:</b> ~{estimated_size_mb:.0f} MB\n\n"
            message += "⚠️ <b>Diqqat:</b> Video hajmi katta bo'lishi mumkin.\n"
            message += "Agar yuborilmasa, pastroq sifat yoki Direct Link tanlang.\n\n"
        else:
            message += "\n"
        
        message += "Sifat yoki formatni tanlang:"
        
        await processing_msg.edit_text(
            message,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        
    except Exception as e:
        logger.error(f"URL qayta ishlashda xato: {e}")
        await processing_msg.edit_text(
            "❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring yoki boshqa link yuboring."
        )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tugma bosilganda ishlaydigan funksiya"""
    query = update.callback_query
    await query.answer()
    
    url = context.user_data.get('video_url')
    if not url:
        await query.edit_message_text("❌ Xatolik: Video linki topilmadi. Qaytadan link yuboring.")
        return
    
    # Yuklanish xabarini ko'rsatish
    await query.edit_message_text("⏳ Yuklab olish boshlandi... Iltimos kuting.")
    
    try:
        # Callback data dan sifat yoki formatni olish
        callback_data = query.data
        
        if callback_data.startswith('quality_'):
            quality = callback_data.replace('quality_', '')
            await download_video(query, url, quality)
        elif callback_data == 'format_mp3':
            await download_audio(query, url)
        elif callback_data == 'get_direct_link':
            await get_direct_download_link(query, url)
            
    except Exception as e:
        logger.error(f"Yuklab olishda xato: {e}")
        await query.edit_message_text(
            "❌ Yuklab olishda xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring."
        )


async def download_video(query, url: str, quality: str):
    """Video yuklab olish"""
    user_id = query.from_user.id
    output_path = os.path.join(DOWNLOAD_FOLDER, f"{user_id}_%(title)s.%(ext)s")
    
    # Sifatga qarab sozlamalar
    if quality == 'best':
        format_selector = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
    elif quality == '1080p':
        format_selector = 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best'
    elif quality == '720p':
        format_selector = 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best'
    elif quality == '480p':
        format_selector = 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]/best'
    elif quality == '360p':
        format_selector = 'bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[height<=360][ext=mp4]/best'
    else:
        format_selector = 'best[ext=mp4]/best'
    
    ydl_opts = {
        'format': format_selector,
        'outtmpl': output_path,
        'quiet': False,
        'no_warnings': False,
        'merge_output_format': 'mp4',
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web'],
                'skip': ['hls', 'dash']
            }
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        },
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # Faylni yuborish
            if os.path.exists(filename):
                file_size = os.path.getsize(filename)
                
                # Telegram 50MB limit (bot API)
                if file_size > 50 * 1024 * 1024:
                    # Katta fayllar uchun yuklab olish linkini yuborish
                    file_size_mb = file_size / (1024 * 1024)
                    
                    # Faylni saqlash (ixtiyoriy - server bo'lsa)
                    # Hozircha faqat xabar yuboramiz
                    await query.edit_message_text(
                        f"⚠️ <b>Fayl hajmi juda katta!</b>\n\n"
                        f"📦 Hajm: {file_size_mb:.1f} MB\n"
                        f"🚫 Telegram limit: 50 MB\n\n"
                        f"💡 <b>Yechimlar:</b>\n"
                        f"1. Pastroq sifatni tanlang (480p, 360p)\n"
                        f"2. MP3 formatni tanlang (audio)\n"
                        f"3. To'g'ridan-to'g'ri linkdan yuklab oling:\n\n"
                        f"🔗 <code>{url}</code>\n\n"
                        f"<i>Linkni brauzerda oching va videoni yuklab oling</i>",
                        parse_mode='HTML'
                    )
                    os.remove(filename)
                    return
                
                await query.edit_message_text("📤 Fayl yuborilmoqda...")
                
                with open(filename, 'rb') as video_file:
                    await query.message.reply_video(
                        video=video_file,
                        caption=f"✅ Video yuklab olindi!\n\n📝 {info.get('title', 'Video')}\n🎬 Sifat: {quality}",
                        supports_streaming=True
                    )
                
                await query.edit_message_text("✅ Video muvaffaqiyatli yuborildi!")
                
                # Faylni o'chirish
                os.remove(filename)
            else:
                await query.edit_message_text("❌ Fayl topilmadi.")
                
    except Exception as e:
        logger.error(f"Video yuklab olishda xato: {str(e)}")
        logger.error(f"Quality: {quality}, URL: {url}")
        error_msg = str(e)[:100]
        await query.edit_message_text(
            f"❌ Yuklab olishda xatolik yuz berdi.\n\n"
            f"Xato: {error_msg}\n\n"
            f"💡 Qaytadan urinib ko'ring yoki boshqa sifatni tanlang."
        )


async def download_audio(query, url: str):
    """Audio (MP3) yuklab olish"""
    user_id = query.from_user.id
    output_path = os.path.join(DOWNLOAD_FOLDER, f"{user_id}_%(title)s.%(ext)s")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'no_warnings': False,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web'],
                'skip': ['hls', 'dash']
            }
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        },
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # MP3 fayl nomi
            base_filename = ydl.prepare_filename(info)
            filename = os.path.splitext(base_filename)[0] + '.mp3'
            
            # Faylni yuborish
            if os.path.exists(filename):
                file_size = os.path.getsize(filename)
                
                # Telegram 50MB limit
                if file_size > 50 * 1024 * 1024:
                    await query.edit_message_text(
                        "❌ Fayl hajmi juda katta (>50MB)."
                    )
                    os.remove(filename)
                    return
                
                await query.edit_message_text("📤 Audio yuborilmoqda...")
                
                with open(filename, 'rb') as audio_file:
                    await query.message.reply_audio(
                        audio=audio_file,
                        caption=f"✅ Audio yuklab olindi!\n\n📝 {info.get('title', 'Audio')}\n🎵 Format: MP3",
                        title=info.get('title', 'Audio'),
                        performer=info.get('uploader', 'Unknown')
                    )
                
                await query.edit_message_text("✅ Audio muvaffaqiyatli yuborildi!")
                
                # Faylni o'chirish
                os.remove(filename)
            else:
                await query.edit_message_text("❌ Fayl topilmadi.")
                
    except Exception as e:
        logger.error(f"Audio yuklab olishda xato: {str(e)}")
        logger.error(f"URL: {url}")
        error_msg = str(e)[:100]
        await query.edit_message_text(
            f"❌ Yuklab olishda xatolik yuz berdi.\n\n"
            f"Xato: {error_msg}\n\n"
            f"💡 Qaytadan urinib ko'ring yoki video formatini tanlang."
        )


async def get_direct_download_link(query, url: str):
    """To'g'ridan-to'g'ri yuklab olish linkini olish (katta fayllar uchun)"""
    try:
        await query.edit_message_text("⏳ Yuklab olish linklari tayyorlanmoqda...")
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],
                    'skip': ['hls', 'dash']
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            },
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            title = info.get('title', 'Video')
            formats = info.get('formats', [])
            
            # Eng yaxshi video formatlarni topish
            video_formats = []
            for f in formats:
                if f.get('vcodec') != 'none' and f.get('url'):
                    height = f.get('height', 0)
                    ext = f.get('ext', 'mp4')
                    filesize = f.get('filesize', 0)
                    
                    if height and height >= 360:  # Faqat 360p va yuqori
                        video_formats.append({
                            'height': height,
                            'url': f['url'],
                            'ext': ext,
                            'filesize': filesize or 0
                        })
            
            # Sifat bo'yicha saralash
            video_formats.sort(key=lambda x: x['height'], reverse=True)
            
            # Xabar tayyorlash
            message = f"🎬 <b>{title[:50]}...</b>\n\n"
            message += "✅ <b>KATTA FAYLLAR UCHUN YECHIM!</b>\n\n"
            message += "📥 <b>To'g'ridan-to'g'ri yuklab olish linklari:</b>\n"
            message += "<i>Hajm cheklovi yo'q - 1 GB, 2 GB, 5 GB istalgan hajm!</i>\n\n"
            
            # Eng yaxshi 5 ta formatni ko'rsatish
            shown_heights = set()
            link_count = 0
            
            for fmt in video_formats[:10]:
                height = fmt['height']
                if height not in shown_heights and link_count < 5:
                    shown_heights.add(height)
                    link_count += 1
                    
                    size_mb = fmt['filesize'] / (1024 * 1024) if fmt['filesize'] else 0
                    size_gb = size_mb / 1024
                    
                    if size_gb >= 1:
                        size_text = f" ({size_gb:.2f} GB) 🔥"
                    elif size_mb > 0:
                        size_text = f" ({size_mb:.1f} MB)"
                    else:
                        size_text = ""
                    
                    message += f"🎬 <b>{height}p</b>{size_text}\n"
                    message += f"<code>{fmt['url'][:100]}...</code>\n\n"
            
            if not video_formats:
                message += "❌ Yuklab olish linklari topilmadi.\n\n"
                message += f"Asl link: <code>{url}</code>"
            else:
                message += "\n📱 <b>QANDAY FOYDALANISH (Oddiy 3 qadam):</b>\n\n"
                message += "1️⃣ <b>Linkni nusxalang</b>\n"
                message += "   • Linkni bosib ushlab turing\n"
                message += "   • 'Copy' tugmasini bosing\n\n"
                message += "2️⃣ <b>Brauzerda oching</b>\n"
                message += "   • Chrome, Safari, Firefox - istalgan brauzer\n"
                message += "   • Linkni address barga joylashtiring\n\n"
                message += "3️⃣ <b>Yuklab oling!</b>\n"
                message += "   • Video avtomatik yuklanadi\n"
                message += "   • Istalgan hajm - cheklov yo'q!\n\n"
                message += "💾 <b>Afzalliklari:</b>\n"
                message += "✅ Hajm cheklovi yo'q (1 GB, 2 GB, 5 GB+)\n"
                message += "✅ Telegram orqali emas, to'g'ridan-to'g'ri serverdan\n"
                message += "✅ Tezroq yuklanadi\n"
                message += "✅ Sifat yo'qolmaydi\n\n"
                message += "<i>⚠️ Linklar vaqtinchalik (bir necha soat amal qiladi)</i>"
            
            await query.edit_message_text(message, parse_mode='HTML')
            
    except Exception as e:
        logger.error(f"Direct link olishda xato: {str(e)}")
        logger.error(f"URL: {url}")
        await query.edit_message_text(
            f"❌ Linkni olishda xatolik yuz berdi.\n\n"
            f"Asl link: <code>{url}</code>\n\n"
            f"<i>Ushbu linkni brauzerda oching va videoni yuklab oling</i>",
            parse_mode='HTML'
        )


def main():
    """Botni ishga tushirish"""
    # Application yaratish
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Handlerlarni qo'shish
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Botni ishga tushirish
    logger.info("Bot ishga tushirildi...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
