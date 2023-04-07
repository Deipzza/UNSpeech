import telebot
from flask import Flask, request, session
from flask import render_template
from constants import *
from utils import *

from bot_functions.university_calendar import *
from bot_functions.directory import *
from bot_functions.login import *

import list_message as messages

# Bot creation
bot = telebot.TeleBot(BOT_TOKEN, threaded = False)
bot.set_webhook(url = URL)

# Server initialization
app = Flask(__name__,
            static_folder='assets',)


"""------------------------------message-----------------------------------"""
# Start message handler
@bot.message_handler(commands = ["start"])
def start_handler(message):
  """Returns the message that the user receives
  after sending the /start command.
  """

  bot.send_message(message.chat.id, messages.welcome, parse_mode = "Markdown")

# List of commands message handler
@bot.message_handler(commands = ["comandos"])
def commands_handler(message):
  """Returns the message that the user receives
  after sending the /start command.
  """

  bot.send_message(message.chat.id, messages.list_comands)

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

    menu = [
        {"name": "Pregrado", "value": "so_pregrado"}, 
        {"name": "Posgrado", "value": "so_posgrado"}
    ]
    bot.send_message(message.chat.id, "¿Qué tipo de estudiante eres?", reply_markup = gen_markup(menu))

# Request calendar message handler
@bot.message_handler(commands = ["informacion_sia"])
def initial_sia(message):
    """ """

    menu = [
      {"name": "Mi historia académica", "value": "sia_academic_history"},
      {"name": "Mi Horario", "value": "sia_schedule"}
    ]
    bot.send_message(message.chat.id, "¿Qué deseas consultar?", reply_markup = gen_markup(menu))

"""------------------------------callback-----------------------------------"""
# Interactive messages for academic calendar handler
@bot.callback_query_handler(func=lambda call: call.data in ["ac_pregrado", "ac_posgrado"])
def callback_query(call):
    bot.answer_callback_query(call.id, messages.time_out)  
    calendar = generate_academic_calendar(call.data[3:])
    bot.send_message(call.message.chat.id, "*Calendario académico.*\n" + calendar, parse_mode = "Markdown")

# Interactive messages for requests calendar handler
@bot.callback_query_handler(func = lambda call: call.data in ["so_pregrado","so_posgrado"])
def callback_query(call):
    bot.answer_callback_query(call.id, messages.time_out)  
    calendar = generate_request_calendar(call.data[3:])
    bot.send_message(call.message.chat.id, "*Calendario de solicitudes.*\n" + calendar, parse_mode = "Markdown")

# Interactive messages for requests calendar handler
@bot.callback_query_handler(func = lambda call: "sia" in call.data)
def callback_query(call):
    #bot.answer_callback_query(call.id, messages.time_out)
    initial_login = f"""
Para poder obtener la información del SIA necesitamos que ingreses al link:
[http://localhost:10000/login](http://localhost:10000/login)

Utiliza este token para poder autenticarte:
{call.message.chat.id}
Mantén tu token seguro y guárdalo en un lugar seguro, ya que puede ser utilizado por cualquiera para acceder.
"""
    bot.send_message(call.message.chat.id, initial_login, parse_mode = "Markdown")


# Request directorio message handler
@bot.message_handler(commands = ["directorio"])
def requests_directorio(message):
    
    text = "Escribe las palabras clave para buscar en el directorio, separadas por espacios.\nPor ejemplo: bienestar minas facultad"
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, requests_directorio_handler, bot)

# Request groups list message handler
@bot.message_handler(commands = ["buscar_grupos"])
def requests_groups(message):

    text = "Escribe el código de la asignatura de la cual quieres buscar un grupo."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, search_groups_handler, bot)

# Add groups message handler
@bot.message_handler(commands = ["agregar_grupos"])
def add_groups(message):
    
    text = "Escribe el código de la asignatura de la cual quieres agregar el grupo."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, add_groups_name_handler, bot)

# Handler for other messages
@bot.message_handler(func = lambda msg: True)
def echo_all(message):
    bot.send_message(message.chat.id, "No reconozco ese comando.\nPara ver mi lista de comandos escribe /comandos", parse_mode = "Markdown")



"""------------------------------Flask links-----------------------------------"""
# Server settings
@app.route('/', methods=["POST"])
def webhook():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
    )
    return "ok"

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        chat_id = request.form['token']

        
        payload = {
            "username": username, 
            "password": password
        }
        logged, request_seccion = auth(payload)
        
        if logged:
            driver = login2(payload)
            papa = scraping(driver)
            bot.send_message(chat_id, f"Hola, {username} tu papa es: {papa}")
            #session["sesion"] = request_seccion
        else:
            bot.send_message(chat_id, f"Lo siento, no hemos podido autenticarte. Proba nuevamente.")
        
    return render_template('login.html')

if __name__ == "__main__":
    app.run(port = int(os.environ.get('PORT', 10000))) # Server execution port