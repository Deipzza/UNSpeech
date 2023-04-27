import datetime
import locale
from bson import ObjectId

from .database.mongodatabase import *

# Set the locale to Spanish and Colombian locale
locale.setlocale(locale.LC_ALL, 'es_CO.utf8')

def add_task(data):
    """Inserts a task into the database with the given fields.

    Inputs:
    username -> string with the name of the user that sent the data.
    name -> string with the name of the task.
    description -> string with the description of the task.
    date -> datetime with the date of the task.
    notification_time -> dictionary with the information for the task's alert.
    subject -> string with the name of the subject of the task.
    """

    # Get or create collection
    collection = mongo_db["tasks"]

    # Organize and insert the data
    item = {
        "username": verify_field_null(data["username"]),
        "name": verify_field_null(data["name"]),
        "description": verify_field_null(data["description"]),
        "subject": verify_field_null(data["subject"]),
        "date": verify_field_null(data["date"]),
        "notification_time": verify_field_null(data["notification_time"]),
    }
    
    try:
        collection.insert_one(item)
        return True
    except:
        return False

def update_task(data, id):
    """Updates the task of the given ID.

    Inputs:
    data -> data to be updated.
    id -> id of the task to be updated.
    """

    collection = mongo_db["tasks"]

    query = {"_id": ObjectId(id)}
    update = {"$set": {
        "username": verify_field_null(data["username"]),
        "name": verify_field_null(data["name"]),
        "description": verify_field_null(data["description"]),
        "subject": verify_field_null(data["subject"]),
        "date": verify_field_null(data["date"]),
        "notification_time": verify_field_null(data["notification_time"]),
    }}
    try:
        collection.update_one(query, update)
        return True
    except:
        return False
    
def remove_task(id):
    """Removes the task of the given ID.

    Inputs:
    id -> id of the task to be removed.
    """

    collection = mongo_db["tasks"]
    query = {"_id": ObjectId(id)}

    try:
        collection.delete_one(query)
        return True
    except:
        return False
    
def verify_field_null(field):
    if field == "" or field == "undefined":
        return None
    return field

def task_add(id, data):
    """Adds or updates the task."""

    try:
        ObjectId(id) # Checks if it's a valid ID object
        return update_task(data, id)
    except:
        return add_task(data)

def get_dateless_tasks(username):
    """Returns a list of the tasks that don't have date.
    
    Inputs:
    username -> string.
    """

    # Create query for the search
    query = {
        "$or": [
            {"date": {"$type": 10}},  # Verificar nulo (tipo 10)
            {"date": ""}  # Verificar cadena vacía
        ],
        "username": username,
        
    }

    results = select_query_tasks(query) # Make the search
    task_list = parse_task_list(results) # Format the results

    return task_list

"""----------------------David funciones----------------------"""
def insert_values_into_tasks(username, name, description = None,
                             date = None, notification_time = None,
                             subject = None):
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

    return item
        
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
        "subject": 1
    }

    # Run query
    results = mongo_db.tasks.find(query, projection)

    # if mongo_db.tasks.count_documents(query) < 1:
    #     return "No tienes tareas guardadas."

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