import telebot
from telebot import types
from flask import Flask, request
from constant import *
from academic_calendad_V2 import get_calendar
from utils import gen_markup

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
bot.set_webhook(url=URL)

app = Flask(__name__)

##Bot

@bot.message_handler(commands=['hello'])
def send_welcome(message):
    bot.send_message(message.chat.id , "Howdy, how are you doing?")

# Start message
@bot.message_handler(commands=["start"])
def start_handler(message):
  bot.reply_to(message, 
    """
¡Hola!
Me llamo AllUNBot, soy un bot académico y estoy aquí para ayudarte a tener tu información académica a la mano.

Cuento con varias funcionalidades que pueden serte útiles, solo tienes que escribir el comando correspondiente 
(o pulsarlo en mi mensaje) y seguir los pasos que te indique.

Para comenzar escribe /comandos
    """)

# List of commands
@bot.message_handler(commands=["comandos"])
def start_handler(message):
  bot.reply_to(message,
  """
===============
FUNCIONALIDADES
===============

*Información general*
- Si quieres ver el calendario académico, escribe /calendario_academico

  """
  )


@bot.message_handler(commands=["calendario_academico"])
def academic_calendar(message):
  bot.send_message(message.chat.id, "¿Qué tipo de estudiante eres?", reply_markup=gen_markup())


@bot.callback_query_handler(func=lambda call: call.data.lower() in ["pregrado","posgrado"])
def callback_query(call):
    bot.answer_callback_query(call.id,"Espera a que se genera la respuesta")  
    calendar = get_calendar(call.data)
    bot.send_message(call.message.chat.id, calendar, parse_mode="Markdown")


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, "No reconocemos ese comando.")


##NO BORRAR
@app.route('/', methods=["POST"])
def webhook():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
    )
    return "ok"

if __name__ == "__main__":
    app.run(port=int(os.environ.get('PORT', 10000)))