import os
import threading
import telebot
import requests
from flask import Flask
from waitress import serve

BOT_TOKEN = os.environ.get('BOT_TOKEN')
# Multithreading සමඟ වැඩ කිරීමට threaded=True දීම අත්‍යවශ්‍ය වේ
bot = telebot.TeleBot(BOT_TOKEN, threaded=True)

app = Flask('')

@app.route('/')
def home():
    print("Ping received from UptimeRobot! Server is awake.")
    return "TikTok Telegram Bot is Running Live 24/7! 🚀"

# Flask Web Server එක Background Thread එකක Run කිරීම (Waitress සමඟ)
def run_web_server():
    # Render, Koyeb හෝ GitHub Actions port පරීක්ෂා කිරීම සඳහා port 8080 භාවිතා කරයි
    port = int(os.environ.get("PORT", 8080))
    serve(app, host='0.0.0.0', port=port)

# Telegram Bot Start Message
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🅃🄸🄺🅃🄾🄺 🄳🄾🅆🄽🄻🄾🄰🄳🄴🅁🔥🗿 🙈\n\n"
        "𝚃𝙸𝙺𝚃𝙾𝙺 𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳𝙴𝚁 𝙱𝙾𝚃🧚‍♂️🎀\n\n"
        "Ꭷ ʙᴏᴛ ᴜꜱᴇʀ ɴᴀᴍᴇ :- @rika_ttdl_bot\n"
        "Ꭷ ʙᴏᴛ ʟɪɴᴋ :- https://t.me/rika_ttdl_bot\n\n"
        "𝙳ᴇᴠ :- @Ch4cky_bea 🇱🇰\n\n"
        "⚡ HD Quality\n"
        "🚫 No Watermark\n"
        "🎵 Music Support\n"
        "📊 Video Information\n"
        "🚀 Fast Download\n\n"
        "🔗 𝗖𝗛𝗔𝗡𝗡𝗘𝗟 𝗟𝗜𝗡𝗞🇱🇰࿐ 🔗\n"
        "https://whatsapp.com/channel/0029VbCQggsAYlUMK1VwZb0d\n\n"
        "ᴍᴀᴅᴇ ʙʏ ᴄʜᴜᴄᴋʏ ᴛᴇᴀᴍ 🐻\n"
        "𝙿𝙾𝚆𝙴𝚁𝙳 𝙱𝚈 𝙲𝙷𝚄𝙲𝙺𝚈 🍒🫶"
    )
    bot.reply_to(message, welcome_text, disable_web_page_preview=True)

# TikTok Link එකක් ලැබුණු විට Video එක ඩවුන්ලෝඩ් කිරීම
@bot.message_handler(func=lambda message: True)
def download_tiktok(message):
    url = message.text.strip()
    if "tiktok.com" not in url:
        bot.reply_to(message, "කරුණාකර නිවැරදි TikTok Link එකක් එවන්න💥🖐️.")
        return

    msg = bot.reply_to(message, "⏳ 𝐏𝐋𝐄𝐀𝐒𝐄 𝐖𝐀𝐈𝐓... 𝐅𝐄𝐓𝐂𝐇𝐈𝐍𝐆 𝐕𝐈𝐃𝙴𝙾 🚀")

    try:
        if "vt.tiktok.com" in url or "vm.tiktok.com" in url:
            try:
                r = requests.head(url, allow_redirects=True, timeout=5)
                url = r.url
            except:
                pass

        api_url = f"https://tikwm.com/api/?url={url}&hd=1"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(api_url, headers=headers, timeout=10).json()

        if response.get('code') == 0:
            data = response['data']
            video_url = data.get('hdplay') or data.get('play')
            audio_url = data.get('music')
            title = data.get('title', 'No Title')
            author = data.get('author', {}).get('nickname', 'Unknown')
            likes = data.get('digg_count', 0)

            caption = (
                f"✨ *ᴠɪᴅᴇᴏ ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜰᴜʟʟʏ* ✨\n\n"
                f"📝 *Title:* {title}\n"
                f"👤 *Author:* {author}\n"
                f"❤️ *Likes:* {likes}\n\n"
                f"🎀 *ᴘᴏᴡᴇʀᴅ ʙʏ ᴄʜᴜᴄᴋʏ ᴏꜰᴄ* 🎀"
            )

            if video_url:
                bot.send_video(message.chat.id, video_url, caption=caption, parse_mode='Markdown')
            
            if audio_url:
                bot.send_audio(message.chat.id, audio_url, title="TikTok Audio 🎵", caption="🎀 *ᴘᴏᴡᴇʀᴅ ʙʏ ᴄʜᴜᴄᴋʏ ᴏꜰᴄ* 🎀", parse_mode='Markdown')
            
            bot.delete_message(message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("ᴘʟᴇᴀꜱᴇ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ʟɪɴᴋ👀. Video not found.", chat_id=message.chat.id, message_id=msg.message_id)
    except Exception as e:
        bot.edit_message_text("⚠️ ᴅᴏᴡɴʟᴏᴀᴅ ꜰᴀɪʟᴇᴅ. ᴘʟᴇᴀꜱᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.", chat_id=message.chat.id, message_id=msg.message_id)

if __name__ == "__main__":
    # 1. Flask Web Server එක වෙනම Thread එකක පණ ගැන්වීම
    server_thread = threading.Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()
    print("Waitress Web Server started on port 8080...")

    # 2. Telegram Bot එක Infinity Polling මඟින් ධාවනය කිරීම
    print("Telegram Bot is polling...")
    bot.infinity_polling(allowed_updates=telebot.util.update_types)
