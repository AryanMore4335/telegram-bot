import telebot
import yt_dlp
import os
from telebot import types

TOKEN = "7757411907:AAGaYXArUQbz6qC14SUd12kLe05MW9oYGY0"
ADMIN_ID = 7757026734
CHANNEL = "@Aryan_Vaishu"

bot = telebot.TeleBot(TOKEN)

users = set()

def check_join(user_id):
    try:
        member = bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member","administrator","creator"]
    except:
        return False


@bot.message_handler(commands=['start'])
def start(message):

    if not check_join(message.chat.id):

        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(
            "Join Channel",
            url=f"https://t.me/{CHANNEL.replace('@','')}"
        )

        markup.add(button)

        bot.send_message(
            message.chat.id,
            "⚠️ Join our channel to use the bot",
            reply_markup=markup
        )
        return

    users.add(message.chat.id)

    bot.send_message(
        message.chat.id,
        "Send Instagram Reel Link"
    )


@bot.message_handler(commands=['stats'])
def stats(message):

    if message.chat.id == ADMIN_ID:
        bot.send_message(
            message.chat.id,
            f"👥 Total Users: {len(users)}"
        )


@bot.message_handler(commands=['broadcast'])
def broadcast(message):

    if message.chat.id != ADMIN_ID:
        return

    text = message.text.replace("/broadcast ", "")

    for user in users:
        try:
            bot.send_message(user, text)
        except:
            pass


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


bot.infinity_polling()
