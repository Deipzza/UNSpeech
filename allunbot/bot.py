import json
import os

import telebot
from flask import Flask, jsonify, request, session
from flask import render_template

from bot_functions.university_calendar import *
from bot_functions.login import *
from bot_functions.academic_history import *
from bot_functions.metrics import *
from bot_functions.schedule import *
from bot_functions.calculator import *
from constants import *
import messages_list as messages
from utils import *

# Bot creation
bot = telebot.TeleBot(BOT_TOKEN, threaded = False)
bot.set_webhook(url = URL)

# Server initialization
app = Flask(__name__, static_folder = 'assets',)


"""------------------------------ MESSAGES ----------------------------------"""


@bot.message_handler(commands = ["start"])
def start_handler(message):
    """Start message handler.
    
    Returns (sends) the corresponding message when the user sends
    the /start command.

    Inputs:
    message -> string with the user's message.
    """

    bot.send_message(message.chat.id, messages.welcome, parse_mode = "Markdown")


@bot.message_handler(commands = ["comandos"])
def commands_handler(message):
    """List of commands message handler.
    
    Returns (sends) the corresponding message when the user sends
    the /commandos command.

    Inputs:
    message -> string with the user's message.
    """

    bot.send_message(message.chat.id, messages.commands_list)


@bot.message_handler(commands = ["calendario_academico"])
def academic_calendar(message):
    """Academic calendar message handler.

    Returns (sends) an interactive menu for the user to select
    its student type to load its corresponding academic calendar.

    Inputs:
    message -> string with the user's message.
    """

    menu = [
        {"name": "Pregrado","value": "ac_pregrado"},
        {"name": "Posgrado", "value": "ac_posgrado"},
    ]
    bot.send_message(message.chat.id,
                     "¿Qué tipo de estudiante eres?",
                     reply_markup = gen_markup(menu))


@bot.message_handler(commands = ["calendario_solicitudes"])
def requests_calendar(message):
    """Request calendar message handler.
    
    Returns (sends) an interactive menu for the user to select
    its student type to load its corresponding requests calendar.

    Inputs:
    message -> string with the user's message.
    """

    menu = [
        {"name": "Pregrado", "value": "so_pregrado"}, 
        {"name": "Posgrado", "value": "so_posgrado"}
    ]
    bot.send_message(message.chat.id,
                    "¿Qué tipo de estudiante eres?",
                    reply_markup = gen_markup(menu))


@bot.message_handler(commands = ["informacion_sia"])
def initial_sia(message):
    """Academic information message handler.
    
    Returns an interactive menu for the user to select
    the academic information that wants to receive.

    Inputs:
    message -> string with the user's message.
    """

    username = get_user_by_chat(message.chat.id) # Retrieves the user
    
    if username == "": # If it's not in the DB, authenticate it
        auth_user(message, bot)
    else: # If it's already in the DB, return the interactive menu
        menu = [
            {"name": "Mi historia académica", "value": "sia_academic_history"},
            {"name": "Mi Horario", "value": "sia_schedule"}
        ]
        bot.send_message(message.chat.id,
                        "¿Qué deseas consultar?",
                        reply_markup = gen_markup(menu))


@bot.message_handler(commands = ["directorio"])
def requests_directorio(message):
    """Request directory message handler.
    
    Returns a message for the user to search for the directory.

    Inputs:
    message -> string with the user's message.
    """

    text = messages.search_directory
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, requests_directorio_handler, bot)


@bot.message_handler(commands = ["buscar_grupos"])
def requests_groups(message):
    """Request groups list message handler.
    
    Returns an interactive menu for the user to select
    the academic information that wants to receive.

    Inputs:
    message -> string with the user's message.
    """

    text = "Escribe el código de la asignatura de la cual quieres buscar un grupo."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode = "Markdown")
    bot.register_next_step_handler(sent_msg, search_groups_handler, bot)


@bot.message_handler(commands = ["agregar_grupos"])
def add_groups(message):
    """Add groups message handler.

    """

    text = "Escribe el código de la asignatura de la cual quieres agregar el grupo."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode = "Markdown")
    bot.register_next_step_handler(sent_msg, add_groups_name_handler, bot)

@bot.message_handler(commands = ["actualizar_info_sia"])
def update_info_sia(message):
    """
    """

    text = f"""
Para poder actualizar tu información del SIA necesitamos que ingreses al link:
http://localhost:10000/actualizar

Utiliza este token para poder autenticarte:
{message.chat.id}
Mantén tu token seguro y guárdalo en un lugar seguro, ya que puede ser utilizado por cualquiera para acceder.
"""
    bot.send_message(message.chat.id, text, parse_mode = "Markdown")


# Handler for other messages
@bot.message_handler(func = lambda msg: True)
def echo_all(message):
    bot.send_message(message.chat.id, "No reconozco ese comando.\nPara ver mi lista de comandos escribe /comandos", parse_mode = "Markdown")


"""----------------------------- CALLBACKS ----------------------------------"""

# Interactive messages for academic calendar handler
@bot.callback_query_handler(func=lambda call: call.data in ["ac_pregrado", "ac_posgrado"])
def callback_query(call):
    """Callback function for the user request of the academic calendar.

    Inputs:
    call -> string with the user's chat and message information.
    """

    bot.answer_callback_query(call.id, messages.time_out)  
    calendar = generate_academic_calendar(call.data[3:])
    bot.send_message(call.message.chat.id,
                     f"*Calendario académico.*\n{calendar}",
                     parse_mode = "Markdown")

# Interactive messages for requests calendar handler
@bot.callback_query_handler(func = lambda call: call.data in ["so_pregrado", "so_posgrado"])
def callback_query(call):
    """Callback function for the user request of the requests calendar.

    Inputs:
    call -> string with the user's chat and message information.
    """

    bot.answer_callback_query(call.id, messages.time_out)
    calendar = generate_request_calendar(call.data[3:])
    bot.send_message(call.message.chat.id,
                    f"*Calendario de solicitudes.*\n{calendar}",
                    parse_mode = "Markdown")

# Interactive messages for the academic information handler
@bot.callback_query_handler(func = lambda call: "sia" in call.data)
def callback_login(call):
    """Callback function for the user request of the academic information.

    Inputs:
    call -> string with the user's chat and message information.
    """

    username = get_user_by_chat(call.message.chat.id)

    if username != "":
        # Check for the option selected and return the corresponding information
        if call.data == "sia_academic_history":
            filename = generate_academic_history_img(username)

            if "sentimos" not in filename:
                photo = open(filename, 'rb')
                bot.send_photo(call.message.chat.id, photo)
                # os.remove(filename)
            else:
                bot.send_message(call.message.chat.id,
                                filename,
                                parse_mode = "Markdown")
        
        elif call.data == "sia_schedule":
            schedule = generate_schedule_user(username)
            bot.send_message(call.message.chat.id,
                            f'{schedule}',
                            parse_mode = "Markdown")
    else:
        text = messages.not_registered
        bot.send_message(call.message.chat.id, text, parse_mode = "Markdown")


"""--------------------------------- FLASK ----------------------------------"""

# Server settings
@app.route('/', methods=["POST"])
def webhook():
    """
    """

    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
    )
    return "ok"

@app.route('/', methods=['GET'])
def index():
    """Return the index page of the bot."""

    return render_template('index.html')


@app.route('/actualizar', methods = ['GET', 'POST'])
def update():
    """Returns the update (login) page."""

    return login()

@app.route('/login', methods = ['GET', 'POST'])
def login():
    """Returns the login page."""

    if request.method == 'POST':
        # Get the form information
        username = request.form['username']
        password = request.form['password']
        chat_id = request.form['token']

        payload = {
            "username": username, 
            "password": password,
            "chat_id": chat_id
        }

        bot.send_message(chat_id, messages.time_out, parse_mode = "Markdown")
        
        # Send the form information
        logged, driver = auth(payload)
        
        if logged: # If the login is successful, load the student data
            data = get_academic_history(driver)
            academic_history(username, data)

            data = get_subjects(driver)
            calculator(username, data)
            
            data = get_metrics(driver)
            metrics(username, data)

            data = get_schedule(driver)
            schedule(username, data)

            # Send message of the options to retrieve
            bot.send_message(chat_id, f"Hola, {username}")
            menu = [
                {"name": "Mi historia académica","value": "sia_academic_history"},
                {"name": "Mi Horario", "value": "sia_schedule"}
            ]
            bot.send_message(chat_id,
                            "¿Qué deseas consultar?",
                            reply_markup = gen_markup(menu))
        else:
            bot.send_message(chat_id, messages.not_authenticated)
        
    return render_template('login.html')

@app.route('/calculadora', methods = ['GET', 'POST'])
def calculadora():
    """
    """
    
    headers = ["Asignatura", "Créditos", "Tipología", "Calificación", "Acciones"]

    misCalificaciones = [
        {
            "id": "3010440",
            "data_table": ["Calidad de software", "3", "DISCIPLINAR OBLIGATORIA", "1"],
            "notas":[["nombre","10","3"], ["nombre2","50","5"]]
        },
        {
            "id": "3010836",
            "data_table": ["Cátedra de sistemas: una visión histórico-cultural de la computación", "3", "DISCIPLINAR OPTATIVA", "0"],
            "notas":[["nombre","porcentaje","valor"]]
        },
        {
            "id": "3011019",
            "data_table": ["Desarrollo web", "3", "DISCIPLINAR OPTATIVA", "5"],
            "notas":[["nombre","porcentaje","valor"]]
        },
        {
            "id": "3011021",
            "data_table": ["Programación para ingeniería", "3", "DISCIPLINAR OPTATIVA", "4"],
            "notas":[["nombre","porcentaje","valor"]]
        },
        {
            "id": "3010439",
            "data_table": ["Proyecto Integrado de Ingeniería", "3", "DISCIPLINAR OBLIGATORIA", "5"],
            "notas":[["nombre","porcentaje","valor"]]
        }
    ]
        
    return render_template('calculadora.html', headers = headers, misCalificaciones = misCalificaciones)


@app.route('/data_subject', methods = ['POST'])
def get_data_subject():
    """
    """

    sql = "SELECT * FROM calculator WHERE username = ?;"
    result = select_data_query(sql, db, ["cpatinore"])

    misCalificaciones = {
        "3010440": {
            "data_table": ["Calidad de software", "3", "DISCIPLINAR OBLIGATORIA", "1"],
            "notas":[["nombre","10","3"], ["nombre2","50","5"]]
        },
        "3010836": {
            "data_table": ["Cátedra de sistemas: una visión histórico-cultural de la computación", "3", "DISCIPLINAR OPTATIVA", "0"],
            "notas":[["nombre","porcentaje","valor"]]
        },
        "3011019": {
            "data_table": ["Desarrollo web", "3", "DISCIPLINAR OPTATIVA", "5"],
            "notas":[["nombre","porcentaje","valor"]]
        },
        "3011021": {
            "data_table": ["Programación para ingeniería", "3", "DISCIPLINAR OPTATIVA", "4"],
            "notas":[["nombre","porcentaje","valor"]]
        },
        "3010439": {
            "data_table": ["Proyecto Integrado de Ingeniería", "3", "DISCIPLINAR OBLIGATORIA", "5"],
            "notas":[["nombre","porcentaje","valor"]]
        },
        "initial": result
    }
        
    return jsonify(misCalificaciones)

if __name__ == "__main__":
    """Main execution of the program"""
    app.debug = True
    app.run(port = int(os.environ.get('PORT', 10000))) # Server execution port