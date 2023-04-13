import telebot
from flask import Flask, request, session
from flask import render_template
from constants import *
from utils import *

import list_message as messages
from bot_functions.university_calendar import *
from bot_functions.login import *
from bot_functions.academic_history import *
from bot_functions.metrics import *
from bot_functions.schedule import *

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

    menu = [
        {"name": "Pregrado","value": "ac_pregrado"},
        {"name": "Posgrado", "value": "ac_posgrado"},
    ]
    bot.send_message(message.chat.id,
                     "¿Qué tipo de estudiante eres?",
                     reply_markup = gen_markup(menu))

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

# Academic information message handler
@bot.message_handler(commands = ["informacion_sia"])
def initial_sia(message):
    """
    """

    username = get_user_by_chat(message.chat.id)
    
    if username == "":
        auth_user(message, bot)
    else:
        menu = [
            {"name": "Mi historia académica", "value": "sia_academic_history"},
            {"name": "Mi Horario", "value": "sia_schedule"}
        ]
        bot.send_message(message.chat.id,
                        "¿Qué deseas consultar?",
                        reply_markup = gen_markup(menu))


"""------------------------------callback-----------------------------------"""
# Interactive messages for academic calendar handler
@bot.callback_query_handler(func=lambda call: call.data in ["ac_pregrado", "ac_posgrado"])
def callback_query(call):
    bot.answer_callback_query(call.id, messages.time_out)  
    calendar = generate_academic_calendar(call.data[3:])
    bot.send_message(call.message.chat.id,
                     "*Calendario académico.*\n" + calendar,
                     parse_mode = "Markdown")

# Interactive messages for requests calendar handler
@bot.callback_query_handler(func = lambda call: call.data in ["so_pregrado", "so_posgrado"])
def callback_query(call):
    bot.answer_callback_query(call.id, messages.time_out)  
    calendar = generate_request_calendar(call.data[3:])
    bot.send_message(call.message.chat.id,
                     "*Calendario de solicitudes.*\n" + calendar,
                     parse_mode = "Markdown")

# Interactive messages for academic information handler
@bot.callback_query_handler(func = lambda call: "sia" in call.data)
def callback_login(call):
    
    username = get_user_by_chat(call.message.chat.id)

    if username != "":
        if call.data == "sia_academic_history":
            # table = generete_academic_history_user(username)
            # bot.send_message(call.message.chat.id, f'```{table}```', parse_mode="Markdown")

            # metricas = generate_metrics_user(username)
            # bot.send_message(call.message.chat.id, f'```{metricas}```', parse_mode="Markdown")
            
            filename = generate_academic_history_img(username)
            if "sentimos" not in filename:
                photo = open(filename, 'rb')
                bot.send_photo(call.message.chat.id, photo)
                os.remove(filename)
            else:
                bot.send_message(call.message.chat.id, filename, parse_mode = "Markdown")
        
        elif call.data == "sia_schedule":
            schedule = generate_schedule_user(username)
            bot.send_message(call.message.chat.id, f'```{schedule}```', parse_mode = "Markdown")
    else:
        text = "Lo sentimos, no tenemos registro de inicio de sesión de tu parte. Por favor, escribe /informacion_sia para autenticar e intenta nuevamente"
        bot.send_message(call.message.chat.id, text, parse_mode = "Markdown")


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
            "password": password,
            "chat_id": chat_id
        }

        logged, driver = auth(payload)
        
        if logged:
            data = get_academic_history(driver)
            academic_history(username, data)
            
            data = get_metrics(driver)
            metrics(username, data)

            data = get_schedule(driver)
            schedule(username, data)

            bot.send_message(chat_id, f"Hola, {username}")
            menu = [
            {"name": "Mi historia académica", "value": "sia_academic_history"},
            {"name": "Mi Horario", "value": "sia_schedule"}
            ]
            bot.send_message(chat_id, "¿Qué deseas consultar?", reply_markup = gen_markup(menu))
        else:
            bot.send_message(chat_id, f"Lo sentimos, no hemos podido autenticarte. Prueba nuevamente.")
        
    return render_template('login.html')

if __name__ == "__main__":
    app.run(port = int(os.environ.get('PORT', 10000))) # Server execution port