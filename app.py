from flask import Flask, request, Response
import requests
import io
import platform
import os
import logging
import json

app = Flask(__name__)

TOKEN = os.environ.get('TELEGRAM_TOKEN')
 
def tel_parse_message(message):
    print("message-->",message)
    try:
        chat_id = message['message']['chat']['id']
        txt = message['message']['text']
        print("chat_id-->", chat_id)
        print("txt-->", txt)
 
        return chat_id,txt
    except:
        print("NO text found-->>")
 
def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
                'chat_id': chat_id,
                'text': text
                }
   
    r = requests.post(url,json=payload)
    return r

def generate_image(text):
    with requests.Session() as http_client:
        api = CraiyonAPI(model=CraiyonAPI.Model.Drawing)
        result = api.draw(http_client, "", text)
        print(result.images)
    return result.images[0]
 
def tel_send_image(chat_id, txt):
    url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
    payload = {
        'chat_id': chat_id,
        'photo': "https://i.imgur.com/OYWK7pR.jpeg",
        'caption': txt
    }
 
    r = requests.post(url, json=payload)
    return r
 
@ app.route('/', methods=['GET', 'POST'])
def index():
    app.logger.info("index")
    if request.method == 'POST':
        msg = request.get_json()
        try:
            chat_id, txt = tel_parse_message(msg)
            if txt == "hi":
                tel_send_message(chat_id,"Hello, world!")
            elif txt.startswith("image"):
                tel_send_image(chat_id, txt)
 
            else:
                tel_send_message(chat_id, 'from webhook')
        except:
            print("from index-->")
 
        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"
 
if __name__ == '__main__':
    app.run(debug=True)