import telebot
from telebot import types
from flask import Flask, request
from constant import *
from calendar_university import *
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
- Si quieres ver el calendario de solicitudes, escribe /calendario_solicitudes

  """
  )


@bot.message_handler(commands=["calendario_academico"])
def academic_calendar(message):
  menu=[{"name":"Pregrado","value":"ac_pregrado"},{"name":"posgrado","value":"ac_posgrado"},]
  bot.send_message(message.chat.id, "¿Qué tipo de estudiante eres?", reply_markup=gen_markup(menu))

@bot.message_handler(commands=["calendario_solicitudes"])
def academic_calendar(message):
  menu=[{"name":"Pregrado","value":"so_pregrado"},{"name":"posgrado","value":"so_posgrado"},]
  bot.send_message(message.chat.id, "¿Qué tipo de estudiante eres?", reply_markup=gen_markup(menu))


@bot.callback_query_handler(func=lambda call: call.data in ["ac_pregrado","ac_posgrado"])
def callback_query(call):
    bot.answer_callback_query(call.id,"La respuesta tarda un poco en generar. Por favor espere.")  
    calendar = get_academic_calender(call.data[3:])
    bot.send_message(call.message.chat.id, calendar, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data in ["so_pregrado","so_posgrado"])
def callback_query(call):
    bot.answer_callback_query(call.id,"La respuesta tarda un poco en generar. Por favor espere.")  
    calendar = get_request_calender(call.data[3:])
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