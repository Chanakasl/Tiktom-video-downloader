import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from flask import Flask, request

# Vercel Environment Variables වලින් Token එක ලබා ගැනීම
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ---------------------------------------------------------
# ස්වයංක්‍රීයව Webhook Set කිරීමේ කොටස (Fully Automated)
# ---------------------------------------------------------
def auto_set_webhook():
    # Vercel මඟින් ලබාදෙන Project URL එක ගැනීම
    host = os.environ.get('VERCEL_PROJECT_PRODUCTION_URL') or os.environ.get('VERCEL_URL')
    
    if host:
        # Webhook URL එක සැකසීම (HTTPS අනිවාර්යයි)
        webhook_url = f"https://{host}/{BOT_TOKEN}"
        try:
            bot.remove_webhook()
            bot.set_webhook(url=webhook_url)
            print(f"Webhook automatically set to: {webhook_url}")
        except Exception as e:
            print(f"Webhook Error: {e}")

# Server එක Start වෙද්දිම ස්වයංක්‍රීයව Webhook එක Set වේ
auto_set_webhook()
# ---------------------------------------------------------

@app.route('/', methods=['GET'])
def home():
    return "TikTok Bot is Running & Webhook is Auto-Configured! 🚀"

# Telegram එකෙන් එන පණිවිඩ (Updates) භාරගන්නා ස්ථානය
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "OK", 200
    return "Forbidden", 403

# /start කමාන්ඩ් එක සඳහා
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # පින්තූරයේ ඇති ආකාරයටම අලංකාර Welcome Message එක
    welcome_text = (
        "𝘓𝘈𝘚𝘐 𝘛𝘐𝘒𝘛𝘖𝘒 𝘝𝘐𝘋𝘌𝘖 𝘋𝘖𝘞𝘕𝘓𝘖𝘈𝘋𝘌𝘙 𝘉𝘖𝘛 🙈\n\n"
        "TIKTOK VIDEO DOWNLOAD BOT 🎀\n\n"
        "ම BOT USER NAME :- @rika_ttdl_bot\n"
        "ම BOT LINK :- https://t.me/rika_ttdl_bot\n\n"
        "𝘋𝘦𝘷 :- @cyber_shamiya 🍒\n\n"
        "⚡ HD Quality\n"
        "🚫 No Watermark\n"
        "🎵 Music Support\n"
        "📊 Video Information\n"
        "🚀 Fast Download\n\n"
        "🔗 𝘊𝘏𝘈𝘕𝘌𝘓 𝘓𝘐𝘕𝘒 🔗\n"
        "https://whatsapp.com/channel/0029VbCQggsAYlUMK1VwZb0d\n\n"
        "𝘔𝘈𝘋𝘌 𝘉𝘠 𝘚𝘏𝘈𝘔𝘐𝘒𝘈 𝘋𝘌𝘕𝘜𝘞𝘈𝘕 🐻\n"
        "𝘗𝘖𝘞𝘌𝘙𝘋 𝘉𝘠 𝘙𝘐𝘒𝘈 𝘛𝘌𝘈𝘊𝘏 🎀"
    )
    
    # දැනට කිසිදු බොත්තමක් (Inline Buttons) එකතු කර නැත
    # ඔබට අවශ්‍ය නම් පසුව එකතු කළ හැක
    
    bot.reply_to(message, welcome_text, disable_web_page_preview=True)

# Link එකක් එවූ විට Video එක Download කිරීම
@bot.message_handler(func=lambda message: True)
def download_tiktok(message):
    url = message.text
    if "tiktok.com" not in url:
        bot.reply_to(message, "❌ කරුණාකර නිවැරදි TikTok Link එකක් එවන්න.")
        return

    msg = bot.reply_to(message, "⏳ 𝘗𝘭𝘦𝘢𝘴𝘦 𝘞𝘢𝘪𝘵... 𝘍𝘦𝘵𝘤𝘩𝘪𝘯𝘨 𝘝𝘪𝘥𝘦𝘰 🚀")

    try:
        # TikWM API භාවිතයෙන් Video එක ගැනීම
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
                f"✨ *Video Downloaded Successfully* ✨\n\n"
                f"📝 *Title:* {title}\n"
                f"👤 *Author:* {author}\n"
                f"❤️ *Likes:* {likes}\n\n"
                f"🎀 *ᴘᴏᴡᴇʀᴅ ʙʏ ᴄʜᴜᴄᴋʏ ᴏꜰᴄ* 🎀"
            )

            # Video එක යැවීම
            bot.send_video(message.chat.id, video_url, caption=caption, parse_mode='Markdown')
            
            # Audio එක යැවීම
            if audio_url:
                bot.send_audio(message.chat.id, audio_url, title="TikTok Audio 🎵", caption="🎀 *POWERED BY RIKA TEACH* 🎀", parse_mode='Markdown')
            
            # Processing පණිවිඩය මකා දැමීම
            bot.delete_message(message.chat.id, msg.message_id)
        else:
            bot.edit_message_text("ᴘʟᴇᴀꜱᴇ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ʟɪɴᴋ👀.", chat_id=message.chat.id, message_id=msg.message_id)
    except Exception as e:
        bot.edit_message_text("⚠️ ᴇʀʀᴏʀ. ᴛʀʏ ᴀɢᴀɪɴ࿐ .", chat_id=message.chat.id, message_id=msg.message_id)

