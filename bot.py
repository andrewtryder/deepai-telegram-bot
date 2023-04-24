import os
import telebot
import requests
from craiyonapi import CraiyonAPI

API_KEY = '6105613997:AAGMYbpfa5DcHv1Hy1rGGx5SApi39g2glZI'

bot = telebot.TeleBot(API_KEY)

def generate_image(text):
    with requests.Session() as http_client:
        api = CraiyonAPI(model=CraiyonAPI.Model.Drawing)
        result = api.draw(http_client, "", text)
        print(result.images)
    return result.images[0]

@bot.message_handler(commands=['image'])
@bot.channel_post_handler(commands=['image'])
def generate_image_handler(message):
    print(message)
    text = message.text.replace('/image ', '', 1)
    if not text:
        bot.send_message(chat_id=message.chat.id, text='Please enter some text to generate an image from.')
        return
    image_url = generate_image(text)
    bot.send_photo(chat_id=message.chat.id, photo=image_url)

bot.polling(non_stop=True)