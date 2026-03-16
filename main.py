from flask import Flask
from threading import Thread
import telebot
import yt_dlp
import os

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()


TOKEN = "7757411907:AAGaYXArUQbz6qC14SUd12kLe05MW9oYGY0"
ADMIN_ID = 7757026734

# Channel IDs (private/public)
CHANNELS = [
-1002675139027,
-1002525032749,
-1002598154723,
-1002707852857
]

# Join button links
CHANNEL_LINKS = [
"https://t.me/+uSScK7NyYStjYzBl",
"https://t.me/+OCPJ0YEiG3gzNDll",
"https://t.me/+kIUkQr9_zallOGY9",
"https://t.me/+VWAsDBH7fW1jMTdl"
]

bot = telebot.TeleBot(TOKEN)

users = set()

# load users
try:
    with open("users.txt","r") as f:
        for line in f:
            users.add(int(line.strip()))
except:
    pass


def save_user(user_id):
    if user_id not in users:
        users.add(user_id)
        with open("users.txt","a") as f:
            f.write(str(user_id) + "\n")


def is_joined(user_id):

    for channel in CHANNELS:

        try:
            member = bot.get_chat_member(channel,user_id)

            if member.status not in ["member","administrator","creator"]:
                return False

        except:
            return False

    return True


@bot.message_handler(commands=['start'])
def start(message):

    user_id = message.from_user.id
    save_user(user_id)

    if not is_joined(user_id):

        markup = telebot.types.InlineKeyboardMarkup()

        for link in CHANNEL_LINKS:

            btn = telebot.types.InlineKeyboardButton(
                "Join Channel",
                url=link
            )

            markup.add(btn)

        verify_btn = telebot.types.InlineKeyboardButton(
            "✅ Verify Join",
            callback_data="verify_join"
        )

        markup.add(verify_btn)

        bot.send_photo(
            message.chat.id,
            "https://t.me/ggghjhhhjh/11",
            caption="📥 Welcome to Aryan Insta Download Bot\n\nJoin all channels then click VERIFY",
            reply_markup=markup
        )

        return

    bot.send_message(message.chat.id,"📥 Send Instagram Reel Link")


@bot.callback_query_handler(func=lambda call: call.data == "verify_join")
def verify(call):

    user_id = call.from_user.id

    if is_joined(user_id):

        bot.answer_callback_query(call.id,"Verification successful")

        bot.send_message(call.message.chat.id,"✅ Verified\n\nSend Instagram Reel Link")

    else:

        bot.answer_callback_query(call.id,"Join all channels first")


@bot.message_handler(commands=['stats'])
def stats(message):

    if message.from_user.id == ADMIN_ID:

        bot.send_message(
            message.chat.id,
            f"👥 Total Users: {len(users)}"
        )


@bot.message_handler(commands=['broadcast'])
def broadcast(message):

    if message.from_user.id != ADMIN_ID:
        return

    text = message.text.replace("/broadcast ","")

    sent = 0

    for user in users:

        try:
            bot.send_message(user,text)
            sent += 1

        except:
            pass

    bot.send_message(message.chat.id,f"📢 Broadcast sent to {sent} users")


@bot.message_handler(func=lambda m: "instagram.com" in m.text)
def download(message):

    if not is_joined(message.from_user.id):

        bot.send_message(message.chat.id,"⚠️ Join all channels first")
        return

    url = message.text

    bot.send_message(message.chat.id,"⬇️ Downloading video...")

    ydl_opts = {
        'outtmpl': 'video.mp4',
        'format': 'best'
    }

    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        video = open("video.mp4","rb")

        bot.send_video(message.chat.id,video)

        video.close()

        os.remove("video.mp4")

    except:

        bot.send_message(message.chat.id,"❌ Download failed")


keep_alive()
bot.infinity_polling(skip_pending=True)
