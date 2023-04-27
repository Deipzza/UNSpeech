import json
import os

from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required
from flask_login import login_user
import secrets

import telebot

from bot_functions.academic_history import *
from bot_functions.calculator import *
from bot_functions.grades import *
from bot_functions.login import *
from bot_functions.metrics import *
from bot_functions.schedule import *
from bot_functions.university_calendar import *
from bot_functions.task import *
from constants import *
import messages_list as messages
from utils import *

# Bot creation
bot = telebot.TeleBot(BOT_TOKEN, threaded = False)
bot.set_webhook(url = URL)

# Server initialization
app = Flask(__name__, static_folder = 'assets',)
app.secret_key = secrets.token_hex(16)

#Login managger
login_manager = LoginManager(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(username):
    users_collection = mongo_db["user_logged"]
    user_data = users_collection.find_one({'username': username})
    if user_data:
        return User(username=user_data['username'], data = user_data['data'])
    return None
    


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
    print("username: ", username)
    
    if username == "": # If it's not in the DB, authenticate it
        auth_user(message, bot)
    else: # If it's already in the DB, return the interactive menu
        menu = [
            {"name": "Mi historia académica", "value": "sia_academic_history"},
            {"name": "Mi Horario", "value": "sia_schedule"},
            {"name": "Calculadora de notas", "value": "sia_calculator_grades"},
        ]
        bot.send_message(message.chat.id,
                        "¿Qué deseas consultar?",
                        reply_markup = gen_markup(menu))


@bot.message_handler(commands = ["directorio"])
def requests_directory(message):
    """Request directory message handler.
    
    Returns a message for the user to search for the directory.

    Inputs:
    message -> string with the user's message.
    """

    text = messages.search_directory
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, requests_directory_handler, bot)


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

    student = call.data[3:]
    bot.answer_callback_query(call.id, messages.time_out)  
    calendar = generate_academic_calendar(student)
    bot.send_message(call.message.chat.id,
                     f"*Calendario académico de {student}.*\n{calendar}",
                     parse_mode = "Markdown")

# Interactive messages for requests calendar handler
@bot.callback_query_handler(func = lambda call: call.data in ["so_pregrado", "so_posgrado"])
def callback_query(call):
    """Callback function for the user request of the requests calendar.

    Inputs:
    call -> string with the user's chat and message information.
    """

    student = call.data[3:]
    bot.answer_callback_query(call.id, messages.time_out)
    calendar = generate_request_calendar(student)
    bot.send_message(call.message.chat.id,
                    f"*Calendario de solicitudes {student}.*\n{calendar}",
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
            else:
                bot.send_message(call.message.chat.id,
                                filename,
                                parse_mode = "Markdown")
        
        elif call.data == "sia_schedule":
            schedule = generate_schedule_user(username)
            bot.send_message(call.message.chat.id,
                            f'{schedule}',
                            parse_mode = "Markdown")
        elif call.data == "sia_calculator_grades":
            text = f"""
Para poder utilizar la calculadora de notas necesitamos que ingreses al link:
http://localhost:10000/calculadora?token={call.message.chat.id}
Recuerda NO compartir este enlace ya que cualquiera podrá tener acceso a tu información.
"""
            bot.send_message(call.message.chat.id, text, parse_mode = "Markdown")
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
            
            data = get_metrics(driver)
            metrics(username, data)

            data = get_calculator(driver)
            calculator(username, data)

            data = get_grades(driver)
            grades(username, data)

            data = get_schedule(driver)
            schedule(username, data)

            # Send message of the options to retrieve
            bot.send_message(chat_id, f"Hola, {username}")
            menu = [
                {
                    "name": "Mi historia académica",
                    "value": "sia_academic_history"
                },
                {
                    "name": "Mi Horario",
                    "value": "sia_schedule"
                },
                {
                    "name": "Calculadora de notas",
                    "value": "sia_calculator_grades"
                }
            ]
            bot.send_message(chat_id,
                            "¿Qué deseas consultar?",
                            reply_markup = gen_markup(menu))
        else:
            bot.send_message(chat_id, messages.not_authenticated)
        
    return render_template('login.html', logged = False)

@app.route('/actualizar', methods = ['GET', 'POST'])
def update():
    """Returns the update (login) page."""

    return login()


@app.route('/auth_ldap', methods = ['GET', 'POST'])
def auth_ldap_page():
    
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'GET':
        return render_template('auth_ldap.html')

    username = request.form['username']
    password = request.form['password']
    user = auth_ldap(username, password)
    
    if user is not None:
        login_user(user)
        return redirect(url_for('dashboard'))
    else:
        return render_template('auth_ldap.html', logged = False)

@app.route('/dashboard', methods = ['GET', 'POST'])
def dashboard():

    is_auth, info_sia, username = user_authenticated(current_user)
    if not is_auth:
        return redirect(url_for('auth_ldap_page'))

    return render_template('dashboard.html', 
                           username = username, 
                           logged = is_auth, 
                           info_sia = info_sia)

@app.route('/calculadora', methods = ['GET'])
def calculadora():
    """ """
    is_auth, info_sia, username = user_authenticated(current_user)
    if not is_auth:
        return redirect(url_for('auth_ldap_page'))
    
    headers = ["Asignatura", "Créditos", "Tipología", "Calificación", "Acciones"]

    projection_grades = {"_id": 0, "data": 1}
    query = {"username": username}
    my_grades = mongo_db.grades.find(query,
                                     projection_grades)[0]["data"]    

    return render_template('calculadora.html',
                            headers = headers,
                            my_grades = my_grades,
                            username = username,
                            logged = is_auth, 
                            info_sia = info_sia)

@app.route('/tasks', methods = ['GET', 'POST'])
def task():
    is_auth, info_sia, username = user_authenticated(current_user)
    if not is_auth:
        return redirect(url_for('auth_ldap_page'))
    
    return render_template('tasks.html', 
                           username = username, 
                           logged = is_auth, 
                           info_sia = info_sia,
                           tasks_recordatorios = get_dateless_tasks(username),
                           tasks_today = get_today_tasks(username),
                           tasks_upcoming = get_future_tasks(username),
                           tasks_archivados = get_past_tasks(username)
                           )



"""--------------------------------- API ----------------------------------"""
@app.route('/calculadora', methods = ['POST'])
def get_data_subject():
    """
    """
    
    username = request.form['username']
    if username != None:

        projection= {"_id": 0, "data": 1}
        query = {"username": username}
        myGrades = mongo_db.grades.find(query, projection)[0]["data"]

        projection = {
            "_id": 0, 
            "username": 1,
            'plan_estudios': 1,
            'ponderado': 1,
            'fund_op': 1,
            'creditos': 1,
            'suma': 1,
            'size': 1
        }

        myMetrics = mongo_db.calculator.find(query, projection)[0]
        myGrades["initial_metrics"] = myMetrics

        return jsonify(myGrades)
    else:
        return jsonify({})
    
@app.route('/api/task', methods = ['POST'])
def add_task_db():
    """
    """
    
    username = current_user.get_id()
    name = request.form['name']
    id = request.form['id']

    data = request.form.copy()
    data["username"] = username

    if username != None and name != None and id != None:
        item = task_add(id, data)
        return json.dumps(item, default=str)
    else:
        return jsonify({})

@app.route('/api/task', methods = ['DELETE'])
def remove_task_db():
    """
    """

    id = request.form['id']

    if id != None:
        item = remove_task(id)
        return json.dumps(item, default=str)
    else:
        return jsonify({})

if __name__ == "__main__":
    """Main execution of the program"""
    app.debug = True # Hot reloading
    app.run(port = int(os.environ.get('PORT', 10000))) # Server execution port