import json
import os

from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required, logout_user
from flask_login import login_user
import secrets

import telebot

from bot_functions.academic_history import *
from bot_functions.alerts import *
from bot_functions.calculator import *
from bot_functions.events import *
from bot_functions.grades import *
from bot_functions.login import *
from bot_functions.metrics import *
from bot_functions.schedule import *
from bot_functions.tasks import *
from bot_functions.university_calendar import *
from bot_functions.users import *
from constants import *
import messages_list as messages
from bot_utils import *

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
    """Load the user's page if it exists in the database."""

    users_collection = mongo_db["user_logged"]
    user_data = users_collection.find_one({'username': username})

    if user_data:
        return User(username = user_data['username'], data = user_data['data'])

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


@bot.message_handler(commands = ["informacion_academica"])
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
            {"name": "Mi Horario", "value": "sia_schedule"},
            {"name": "Calculadora de notas", "value": "sia_calculator_grades"},
            {"name": "Mis tareas", "value": "sia_my_tasks"},
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

    Returns an interactive menu for the user to write the group's information.

    Inputs:
    message -> string with the user's message.
    """

    text = "Escribe el código de la asignatura de la cual quieres agregar el grupo."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode = "Markdown")
    bot.register_next_step_handler(sent_msg, add_groups_name_handler, bot)


@bot.message_handler(commands = ["agregar_tarea"])
def add_tasks(message):
    """Add tasks message handler.

    Inputs:
    message -> string with the user's message.
    """

    text = f"""
Para agregar una tarea debes ingresar al enlace:
{URL}/tareas
"""
    bot.send_message(message.chat.id, text, parse_mode = "Markdown")


@bot.message_handler(commands = ["actualizar_info_sia"])
def update_info_sia(message):
    """Academic info updater handler.

    Inputs:
    message -> string with the user's message.
    """

    text = f"""
Para poder actualizar tu información del SIA debes ingresar al enlace:
{URL}/actualizar

Utiliza este token para poder autenticarte:
{message.chat.id}
Recuerda guardar tu token en un lugar seguro, ya que puede ser utilizado por cualquiera para acceder.
"""
    bot.send_message(message.chat.id, text, parse_mode = "Markdown")


@bot.message_handler(commands = ["eventos"])
def requests_calendar(message):
    """Events message handler.
    
    Returns (sends) an interactive menu for the user to select
    one option for seeing or managing events.

    Inputs:
    message -> string with the user's message.
    """

    menu = [
        {"name": "Ver eventos de hoy", "value": "today_events"}, 
        {"name": "Ver todos los eventos", "value": "all_events"},
        {"name": "Editar tus eventos", "value": "edit_events"}
    ]
    bot.send_message(message.chat.id,
                    "¿Qué deseas hacer?",
                    reply_markup = gen_markup(menu))


@bot.message_handler(func = lambda msg: True)
def echo_all(message):
    """Message handler for other messages."""

    bot.send_message(message.chat.id, messages.not_recognized,
                     parse_mode = "Markdown")


def send_alert():
    """Sends alert message with their tasks to all users."""

    users = get_users()

    for user in users:
        try: # Check if the user has an active chat with the bot
            tasks = get_user_message_tasks(user)
            if tasks != "": # Only send if user has tasks
                message = f"""
*¡Recuerda!*
Tus notificaciones para hoy son:
{tasks}
"""
                bot.send_message(int(user["chat_id"]), text = message)
        except:
            pass

"""----------------------------- CALLBACKS ----------------------------------"""


@bot.callback_query_handler(func=lambda call: call.data in ["ac_pregrado",
                                                            "ac_posgrado"])
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


@bot.callback_query_handler(func = lambda call: call.data in ["so_pregrado",
                                                              "so_posgrado"])
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
Para poder utilizar la calculadora de notas debes ingresar al enlace:
{URL}/calculadora
"""
            bot.send_message(call.message.chat.id, text,
                             parse_mode = "Markdown")
        elif call.data == "sia_my_tasks":
            text = f"""
Para poder ver tus tareas debes ingresar al enlace:
{URL}/tasks
"""
            bot.send_message(call.message.chat.id, text, parse_mode =
                             "Markdown")
    else:
        text = messages.not_registered
        bot.send_message(call.message.chat.id, text, parse_mode = "Markdown")


@bot.callback_query_handler(func=lambda call: call.data in ["today_events",
                                                            "all_events",
                                                            "edit_events"])
def callback_query(call):
    """Callback function for the user request of the events.

    Inputs:
    call -> string with the user's chat and message information.
    """

    if call.data == "today_events":
        bot.send_message(call.message.chat.id,
                         get_message_today_events())
    elif call.data == "all_events":
        text = f"""
Para ver todos los eventos debes ingresar al enlace:
{URL}/all-events
"""
        bot.send_message(call.message.chat.id, text, parse_mode = "Markdown")
    elif call.data == "edit_events":
        bot.send_message(call.message.chat.id,
                         messages.edit_events)


"""--------------------------------- FLASK ----------------------------------"""


@app.route('/', methods=["POST"])
def webhook():
    """Establish server settings"""

    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
    )
    return "ok"


@app.route('/', methods=['GET'])
def index():
    """Return the index page of the bot."""
    is_auth, _, username, _ = user_authenticated(current_user)

    return render_template('index.html', logged = is_auth, username = username)


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
                },
                {
                    "name": "Mis tareas",
                    "value": "sia_my_tasks"
                }
            ]
            bot.send_message(chat_id,
                            "¿Qué deseas consultar?",
                            reply_markup = gen_markup(menu))
        else:
            bot.send_message(chat_id, messages.not_authenticated)
        
    return render_template('login.html', logged = False)

@app.route('/auth-ldap', methods = ['GET', 'POST'])
def auth_ldap_page():
    """Returns the authentication page."""
    
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
        return render_template('auth_ldap.html',
                               logged = False,
                               error = "Fallo en la autenticación")

@app.route('/actualizar', methods = ['GET', 'POST'])
def update():
    """Returns the update (login) page."""

    return login()

@app.route('/dashboard', methods = ['GET', 'POST'])
def dashboard():
    """Returns the dashboard page for a logged user."""

    is_auth, info_sia, username, permissions = user_authenticated(current_user)

    # If the user is not authenticated, returns the authentication page.
    if not is_auth:
        return redirect(url_for('auth_ldap_page'))
    
    today_events = get_today_events()

    return render_template('dashboard.html', 
                           username = username, 
                           logged = is_auth, 
                           info_sia = info_sia,
                           today_events = today_events,
                           permissions = permissions)


@app.route('/calculadora', methods = ['GET'])
def calculadora():
    """Returns the calculator page for a logged user."""

    is_auth, info_sia, username, permissions = user_authenticated(current_user)

    # If the user is not authenticated, returns the authentication page.
    if not is_auth:
        return redirect(url_for('auth_ldap_page'))
    
    headers = ["Asignatura", "Créditos", "Tipología", "Calificación", "Acciones"]

    projection_grades = {"_id": 0, "data": 1}
    query = {"username": username}
    my_grades = mongo_db.grades.find(query,
                                     projection_grades)[0]["data"]    
    
    today_events = get_today_events()

    return render_template('calculadora.html',
                            headers = headers,
                            my_grades = my_grades,
                            username = username,
                            logged = is_auth, 
                            info_sia = info_sia,
                            today_events = today_events,
                            permissions = permissions)


@app.route('/tasks', methods = ['GET', 'POST'])
def task():
    """Returns the tasks page for a logged user."""

    is_auth, info_sia, username, permissions = user_authenticated(current_user)

    # If the user is not authenticated, returns the authentication page.
    if not is_auth:
        return redirect(url_for('auth_ldap_page'))
    
    today_events = get_today_events()
    
    return render_template('tasks.html', 
                           username = username, 
                           logged = is_auth, 
                           info_sia = info_sia,
                           tasks_recordatorios = get_dateless_tasks(username),
                           tasks_today = get_today_tasks(username),
                           tasks_upcoming = get_future_tasks(username),
                           tasks_archivados = get_past_tasks(username),
                           today_events = today_events,
                           permissions = permissions
                           )


@app.route('/events', methods = ['GET'])
def events():
    """Returns the events page for a logged user."""

    is_auth, info_sia, username, permissions = user_authenticated(current_user)

    # If the user is not authenticated, returns the authentication page.
    if not is_auth or not 1 in permissions:
        return redirect(url_for('auth_ldap_page'))
    
    today_events = get_today_events()

    return render_template('events.html', 
                           username = username, 
                           logged = is_auth, 
                           info_sia = info_sia,
                           events = get_events_by_user(username),
                           today_events = today_events,
                           permissions = permissions
                           )

@app.route('/all-events', methods = ['GET'])
def all_events():
    """Returns the all-events page for a logged user."""

    is_auth, info_sia, username, permissions = user_authenticated(current_user)

    # If the user is not authenticated, returns the authentication page.
    if not is_auth:
        return redirect(url_for('auth_ldap_page'))
    
    today_events = get_today_events()

    return render_template('all_events.html', 
                           username = username, 
                           logged = is_auth, 
                           info_sia = info_sia,
                           events = get_events(),
                           today_events = today_events,
                           permissions = permissions
                           )

@app.route('/create_event', methods = ['GET', 'POST'])
def create_event():
    """Returns the create_event page for a logged user."""

    is_auth, info_sia, username, permissions = user_authenticated(current_user)

    # If the user is not authenticated, returns the authentication page.
    if not is_auth or not 1 in permissions:
        return redirect(url_for('auth_ldap_page'))
    
    today_events = get_today_events()

    return render_template('create_events.html', 
                           username = username, 
                           logged = is_auth, 
                           info_sia = info_sia,
                           today_events = today_events,
                           permissions = permissions
                           )

@app.route('/logout')
@login_required
def logout():
    """Returns the main login page as the logout action is successful."""

    is_auth, _, username, _ = user_authenticated(current_user)

    if not is_auth:
        return redirect(url_for('auth_ldap_page'))

    mongo_db.user_logged.delete_many({"username": username})
    logout_user()

    return redirect(url_for('auth_ldap_page'))


"""--------------------------------- API ----------------------------------"""


@app.route('/calculadora', methods = ['POST'])
def get_data_subject():
    """Gets the actual semester's subjects data from the database for the
    calculator.
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
    """Endpoint for adding tasks."""
    
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
    """Endpoint for removing tasks."""

    id = request.form['id']

    if id != None:
        item = remove_task(id)
        return json.dumps(item, default=str)
    else:
        return jsonify({})


@app.route('/api/event', methods = ['PUT'])
def update_event_db():
    """Endpoint for adding events."""
    
    username = current_user.get_id()
    name = request.form['name']
    id = request.form['id']

    data = request.form.copy()
    data["username"] = username

    if username != None and name != None and id != None:
        item = update_event(id, data)
        return json.dumps(item, default=str)
    else:
        return jsonify({})


@app.route('/api/event', methods = ['DELETE'])
def remove_event_db():
    """Endpoint for removing events."""

    id = request.form['id']

    if id != None:
        item = remove_event(id)
        return json.dumps(item, default=str)
    else:
        return jsonify({})


@app.route('/api/event', methods = ['POST'])
def add_event_db():
    """Endpoint for adding events."""
    
    username = current_user.get_id()
    name = request.form['name']

    data = request.form.copy()
    data["username"] = username

    if username != None and name != None:
        item = add_event(request.form)
        return json.dumps(item, default=str)
    else:
        return jsonify({})

"""--------------------------------- MAIN ----------------------------------"""


if __name__ == "__main__":
    """Main execution of the program"""
    
    create_schedule_thread(send_alert)

    mongo_db.user_logged.delete_many({})
    # app.debug = True # Hot reloading
    app.run(port = int(os.environ.get('PORT', 10000))) # Server execution port