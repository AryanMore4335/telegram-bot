import telebot
import yt_dlp
from flask import Flask
import threading

TOKEN = "7757411907:AAGaYXArUQbz6qC14SUd12kLe05MW9oYGY0"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Send Instagram Reel Link")

@bot.message_handler(func=lambda message: True)
def download(message):
    url = message.text
    bot.reply_to(message, "Downloading video...")

    ydl_opts = {'format': 'mp4'}

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        video = open("video.mp4", "rb")
        bot.send_video(message.chat.id, video)

    except:
        bot.reply_to(message, "Download failed")

app = Flask('')

@app.route('/')
def home():
    return "Bot Running"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

keep_alive()
bot.infinity_polling()
