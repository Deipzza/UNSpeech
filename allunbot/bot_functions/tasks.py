import datetime
import locale

from .database.mongodatabase import *

# Set the locale to Spanish and Colombian locale
locale.setlocale(locale.LC_ALL, 'es_CO.utf8')

def insert_values_into_tasks(username, name, description = "",
                             date = "", notification_time = "",
                             subject = ""):
    """Inserts a task into the database with the given fields.

    Inputs:
    username -> string with the name of the user that sent the data.
    name -> string with the name of the task.
    description -> string with the description of the task.
    date -> datetime with the date of the task.
    notification_time -> dictionary with the information for the task's alert.
    subject -> string with the name of the subject of the task.
    """

    collection = mongo_db["tasks"]

    item = {
        "username": username,
        "name": name,
        "description": description,
        "subject": subject,
        "date": date,
        "notification_time": notification_time,
    }

    collection.insert_one(item)

def select_query_tasks(query):
    """Retrieves the list of tasks for a given username.

    Inputs:
    username -> string

    Returns:
    The list of tasks in message format.
    """

    # Select which fields to retrieve from the query
    projection = {
        "_id": 1, 
        "name": 1,
        "description": 1,
        "date": 1,
        "notification_time": 1,
        "subject": 1,
    }

    # Run query
    results = mongo_db.tasks.find(query, projection)

    if mongo_db.tasks.count_documents(query) < 1:
        return None

    return results

def parse_date(date_input):
    date, time = [x for x in date_input.split(",")]
    year, month, day = [int(x) for x in date.split("-")]
    new_date = datetime.date(year, month, day)
    date_string = new_date.strftime("%B %d, %Y")

    hour, minute = [int(x) for x in time.split(":")]
    new_time = datetime.time(hour, minute)
    time_string = new_time.strftime("%I:%M %p")

    complete_date_string = f"{date_string}. {time_string}"

    return complete_date_string

def get_past_tasks(username):
    """Returns a list of the tasks that already passed.

    Inputs:
    username -> string.
    """

    today = str(datetime.date.today())
    query = {
        "username" : username,
        "date": {"$exists": True},
        "$expr": {
            "$lt": [{"$substr": ["$date", 0, 10]}, today]
        }
    }

    results = select_query_tasks(query) # Make the search

    if results is None:
        return "No tienes tareas."
    
    task_list = parse_task_list(results) # Format the results

    return task_list

def get_today_tasks(username):
    """Returns a list of the tasks that occur the day of the query.

    Inputs:
    username -> string.
    """

    today = str(datetime.date.today())

    # Create query for the search
    query = {
        "$and": [
            {"username": username},
            {"date": {"$regex": f"^{today}"}}
        ]
    }

    results = select_query_tasks(query) # Make the search

    if results is None:
        return "No tienes tareas."
    
    task_list = parse_task_list(results) # Format the results

    return task_list

def get_future_tasks(username):
    """Returns a list of the tasks that haven't occurred.

    Inputs:
    username -> string.
    """

    today = str(datetime.date.today())

    # Create query for the search
    query = {
        "username" : username,
        "date": {"$exists": True},
        "$expr": {
            "$gt": [{"$substr": ["$date", 0, 10]}, today]
        }
    }

    results = select_query_tasks(query) # Make the search

    if results is None:
        return "No tienes tareas."
    
    task_list = parse_task_list(results) # Format the results

    return task_list

def get_dateless_tasks(username):
    """Returns a list of the tasks that don't have date.

    Inputs:
    username -> string.
    """

    # Create query for the search
    query = {
        "$and": [
            {"username": username},
            {"date": ""}
        ]
    }

    results = select_query_tasks(query) # Make the search

    if results is None:
        return "No tienes tareas."
    
    task_list = parse_task_list(results) # Format the results

    return task_list

def parse_task_list(task_list):
    """Format the list of tasks to fill the blank fields.

    Inputs:
    task_list -> MongoDB cursor object with the results of the query.
    Returns:
    list of dictionaries with the tasks.
    """

    formated_list = []

    for task in task_list:
        task["description"] = (
            "" if "description" not in task else task["description"]
        )
        task["subject"] = (
            "" if "subject" not in task else task["subject"]
        )
        task["date"] = (
            "" if "date" not in task else task["date"]
        )
        task["notification_time"] = (
            "" if "notification_time" not in task else task["notification_time"]
        )
        formated_list.append(task)

    return formated_list

def get_user_message_tasks(user):
    """Returns the list of tasks formatted as a message."""

    message = ""
    tasks = get_today_tasks(user["username"])
    
    for task in tasks:
        message += f"\nNombre: {task['name']}\n"
        message += (f"Descripción: {task['description']}\n" 
                    if task['description'] != "" else "")
        message += (f"Materia: {task['subject']}\n" 
                    if task['subject'] != "" else "")
        message += (f"Fecha: {task['date']}\n" 
                    if task['date'] != "" else "")
        message += "--------------------------------"
    
    return message
