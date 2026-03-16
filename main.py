from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
import telebot
import yt_dlp
import os

TOKEN = "7757411907:AAGaYXArUQbz6qC14SUd12kLe05MW9oYGY0"
CHANNEL = "@Aryan_vaishu"
ADMIN_ID = 7757026734

bot = telebot.TeleBot(TOKEN)

users = set()


def is_joined(user_id):
    try:
        member = bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member","administrator","creator"]
    except:
        return False


@bot.message_handler(commands=['start'])
def start(message):

    user_id = message.from_user.id
    users.add(user_id)

    if not is_joined(user_id):

        markup = telebot.types.InlineKeyboardMarkup()

        join_btn = telebot.types.InlineKeyboardButton(
            "Join Channel",
            url=f"https://t.me/{CHANNEL.replace('@','')}"
        )

        markup.add(join_btn)

        bot.send_message(
            message.chat.id,
            "Welcome to Aryan Insta Download Bot\n\nFor use bot join this channel",
            reply_markup=markup
        )
        return

    bot.send_message(message.chat.id,"Send Instagram Reel Link")


@bot.message_handler(commands=['stats'])
def stats(message):

    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id,f"Total Users: {len(users)}")


@bot.message_handler(commands=['broadcast'])
def broadcast(message):

    if message.from_user.id != ADMIN_ID:
        return

    text = message.text.replace("/broadcast ","")

    for user in users:
        try:
            bot.send_message(user,text)
        except:
            pass

    bot.send_message(message.chat.id,"Broadcast Sent")


@bot.message_handler(func=lambda m: "instagram.com" in m.text)
def download(message):

    url = message.text

    bot.send_message(message.chat.id,"Downloading video...")

    ydl_opts = {
        'outtmpl': 'video.mp4',
        'format': 'best'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        video = open("video.mp4",'rb')

        bot.send_video(message.chat.id,video)

        os.remove("video.mp4")

    except:
        bot.send_message(message.chat.id,"Download failed")

keep_alive()
bot.infinity_polling(skip_pending=True)
