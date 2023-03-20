import os

import json
import requests

from django.http import JsonResponse
from django.views import View

from dotenv import load_dotenv

import telebot
from telebot import types

# https://api.telegram.org/bot<token>/setWebhook?url=<url>/webhooks/bot/
class bot(View):
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        load_dotenv(os.path.join(BASE_DIR, 'allunbot/.env'))
        self.BOT_TOKEN = os.environ.get("BOT_TOKEN")

    def post(self, request, *args, **kwargs):
        t_data = json.loads(request.body)
        t_message = t_data["message"]

        bot = telebot.TeleBot(BOT_TOKEN,threaded=False)

        try:
            text = t_message["text"].strip().lower()
        except Exception as e:
            return JsonResponse({"ok": "POST request processed"})

        if text == '/start':
            menu=[{"name":"Mostrar horario","value":"/horario"},{"name":"login","value":"/login"}]
            bot.send_message(t_message["chat"]["id"], text='Las posibles opciones:')
        elif text == "/login":
            bot.send_message(t_message["chat"]["id"],f"*Website*: [click here](http://127.0.0.1:8000/login/6209084966)")
        
        bot.send_message(t_message["chat"]["id"],"El comando no lo reconocemos.")
    
    def display_menu(self,menu):
        keyboard = types.InlineKeyboardMarkup()
        for item in menu:
            aux=types.InlineKeyboardButton(item["name"], callback_data=item["value"])
            keyboard.add(aux)
        return keyboard