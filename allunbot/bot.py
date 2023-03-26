import telebot
from flask import Flask, request
from constants import *
from bot_functions.university_calendar import *
from utils import gen_markup
from bot_functions.directory import *

# Bot creation
bot = telebot.TeleBot(BOT_TOKEN, threaded = False)
bot.set_webhook(url = URL)

# Server initialization
app = Flask(__name__)

# Start message handler
@bot.message_handler(commands = ["start"])
def start_handler(message):
  """Returns the message that the user receives
  after sending the /start command.
  """
  bot.send_message(message.chat.id, 
    """
¡Hola!
Me llamo AllUNBot, soy un bot académico y estoy aquí para ayudarte a tener tu información académica a la mano.

Cuento con varias funcionalidades que pueden serte útiles, solo tienes que escribir el comando correspondiente 
(o pulsarlo en mi mensaje) y seguir los pasos que te indique.

Para comenzar escribe /comandos
    """, parse_mode = "Markdown")

# List of commands message handler
@bot.message_handler(commands = ["comandos"])
def commands_handler(message):
  """Returns the message that the user receives
  after sending the /start command.
  """
  bot.send_message(message.chat.id,
  """
===============
FUNCIONALIDADES
===============

*Información general*
- Si quieres ver el calendario académico, escribe /calendario_academico
- Si quieres ver el calendario de solicitudes, escribe /calendario_solicitudes
- Si quieres consultar el directorio UN, escribe /directorio + palabras claves de busqueda

  """)

# Academic calendar message handler
@bot.message_handler(commands = ["calendario_academico"])
def academic_calendar(message):
  """Returns an interactive menu for the user to select
  its student type to load its corresponding requests calendar.
  """
  menu = [{"name": "Pregrado","value": "ac_pregrado"}, {"name": "Posgrado", "value": "ac_posgrado"},]
  bot.send_message(message.chat.id, "¿Qué tipo de estudiante eres?", reply_markup = gen_markup(menu))

# Request calendar message handler
@bot.message_handler(commands = ["calendario_solicitudes"])
def requests_calendar(message):
  """Returns an interactive menu for the user to select
  its student type to load its corresponding requests calendar.
  """
  menu = [{"name": "Pregrado", "value": "so_pregrado"}, {"name": "Posgrado", "value": "so_posgrado"},]
  bot.send_message(message.chat.id, "¿Qué tipo de estudiante eres?", reply_markup = gen_markup(menu))

# Interactive messages for academic calendar handler
@bot.callback_query_handler(func=lambda call: call.data in ["ac_pregrado", "ac_posgrado"])
def callback_query(call):
    bot.answer_callback_query(call.id, "La respuesta tarda un poco en generar. Por favor espere.")  
    calendar = get_academic_calendar(call.data[3:])
    bot.send_message(call.message.chat.id, "*Calendario académico.*\n" + calendar, parse_mode = "Markdown")

# Interactive messages for requests calendar handler
@bot.callback_query_handler(func = lambda call: call.data in ["so_pregrado","so_posgrado"])
def callback_query(call):
    bot.answer_callback_query(call.id, "La respuesta tarda un poco en generar. Por favor espere.")  
    calendar = get_request_calendar(call.data[3:])
    bot.send_message(call.message.chat.id, "*Calendario de solicitudes.*\n" + calendar, parse_mode = "Markdown")

# Request directorio message handler
@bot.message_handler(commands = ["directorio"])
def requests_directorio(message):
  metadata = message.text.split()[1:]
  response = select_query_directorio(metadata, "allunbot.db")
  if len(response) > 4095:
    for part in range(0, len(response), 4095):
        bot.send_message(message.chat.id, response[part:part+4095])
  else:
      bot.send_message(message.chat.id, response)
  #bot.send_message(message.chat.id, response, parse_mode = "Markdown")


# Handler for other messages
@bot.message_handler(func = lambda msg: True)
def echo_all(message):
    bot.send_message(message.chat.id, "No reconozco ese comando.\nPara ver mi lista de comandos escribe /comandos", parse_mode = "Markdown")

# Server settings
@app.route('/', methods=["POST"])
def webhook():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
    )
    return "ok"

if __name__ == "__main__":
    app.run(port = int(os.environ.get('PORT', 10000))) # Server execution port