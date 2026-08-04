import os
import telebot
import requests
from flask import Flask, request

# Vercel Environment Variables වලින් Token එක ලබා ගැනීම
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# threaded=False අනිවාර්යයි Vercel සඳහා
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "TikTok Bot is Running Successfully! 🚀"

# ---------------------------------------------------------
# Webhook එක Set කිරීමට වෙනම මාර්ගයක් (මෙය එක වරක් පමණක් කළ යුතුය)
# ---------------------------------------------------------
@app.route('/setup', methods=['GET'])
def setup_webhook():
    # Vercel එකේ URL එක ස්වයංක්‍රීයව ගැනීම
    host = os.environ.get('VERCEL_PROJECT_PRODUCTION_URL') or request.host
    webhook_url = f"https://{host}/{BOT_TOKEN}"
    
    try:
        bot.remove_webhook()
        bot.set_webhook(url=webhook_url)
        return f"✅ Webhook Successfully Set To: {webhook_url}"
    except Exception as e:
        return f"❌ Webhook Error: {e}"
# ---------------------------------------------------------

# Telegram එකෙන් එන පණිවිඩ භාරගැනීම
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    if request.is_json:
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "OK", 200
    return "Forbidden", 403

# /start කමාන්ඩ් එක
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

# TikTok Link එකක් එවූ විට
@bot.message_handler(func=lambda message: True)
def download_tiktok(message):
    url = message.text
    if "tiktok.com" not in url:
        bot.reply_to(message, "කරුණාකර නිවැරදි TikTok Link එකක් එවන්න💥🖐️.")
        return

    msg = bot.reply_to(message, "⏳ 𝐏𝐋𝐄𝐀𝐒 𝐖𝐀𝐈𝐓... 𝐅𝐄𝐓𝐂𝐇𝐈𝐍𝐆 𝐕𝐈𝐃𝐄𝐎 🚀")

    try:
        api_url = f"https://www.tikwm.com/api/?url={url}"
        response = requests.get(api_url).json()

        if response.get('code') == 0:
            data = response['data']
            video_url = data['play']
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

            bot.send_video(message.chat.id, video_url, caption=caption, parse_mode='Markdown')
            
            if audio_url:
                bot.send_audio(message.chat.id, audio_url, title="TikTok Audio 🎵", caption="🎀 *ᴘᴏᴡᴇʀᴅ ʙʏ ᴄʜᴜᴄᴋʏ ᴏꜰᴄ* 🎀", parse_mode='Markdown')
            
            bot.delete_message(message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("ᴘʟᴇᴀꜱᴇ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ʟɪɴᴋ👀.", chat_id=message.chat.id, message_id=msg.message_id)
    except Exception as e:
        bot.edit_message_text("⚠️ ᴇʀʀᴏʀ. ᴛʀʏ ᴀɢᴀɪɴ࿐ .", chat_id=message.chat.id, message_id=msg.message_id)
