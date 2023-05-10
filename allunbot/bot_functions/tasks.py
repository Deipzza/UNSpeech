from bson import ObjectId
import datetime
import locale

from .database.mongodatabase import *

# Set the locale to Spanish and Colombian locale
locale.setlocale(locale.LC_ALL, 'es_CO.utf8')

def add_task(data):
    """Inserts a task into the database with the given fields.

    Inputs:
    data -> task object with the corresponding fields

    Returns:
    boolean indicating if the task was inserted
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
    update = {
        "$set": {
            "username": verify_field_null(data["username"]),
            "name": verify_field_null(data["name"]),
            "description": verify_field_null(data["description"]),
            "subject": verify_field_null(data["subject"]),
            "date": verify_field_null(data["date"]),
            "notification_time": verify_field_null(data["notification_time"]),
        }
    }
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
    """Checks if the task is going to be added or updated
    depending on the ID.

    Inputs:
    id -> string with the task identifier.
    data -> dict with the task data.

    Returns:
    boolean that indicates whether the task could be added or updated.
    """

    try:
        ObjectId(id) # Checks if it's a valid ID object
        return update_task(data, id)
    except:
        return add_task(data)


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

    results = mongo_db.tasks.find(query, projection) # Run query

    return results


def parse_date(date_input):
    """Formats the date from the user's input."""

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
        "$and": [
            {"date": {"$ne": None}},  # Verify not null
            {"date": {"$ne": ""}},  # Verify not empty string
            {"$expr": {
                "$lt": [{"$substr": ["$date", 0, 10]}, today]
            }}
        ],
        "username": username,
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


def get_dateless_tasks(username):
    """Returns a list of the tasks that don't have date.

    Inputs:
    username -> string.
    """

    # Create query for the search
    query = {
        "$or": [
            {"date": {"$type": 10}},  # Verify null
            {"date": ""}
        ],
        "username": username,
    }

    results = select_query_tasks(query) # Make the search
    task_list = parse_task_list(results) # Format the results

    return task_list


def get_alert_tasks(username):
    """Returns a list of the tasks that have the alert date on the current day.

    Inputs:
    username -> string.
    """

    today = str(datetime.date.today())

    # Create query for the search
    query = {
        "$and": [
            {"username": username},
            {"notification_time": {"$regex": f"^{today}"}}
        ]
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


def get_user_message_tasks(user):
    """Returns the list of tasks formatted as a message."""

    message = ""
    tasks = get_alert_tasks(user["username"])
    
    for task in tasks:
        message += f"\nNombre: {task['name']}\n"
        message += (f"Descripción: {task['description']}\n" 
                    if task['description'] != None else "")
        message += (f"Materia: {task['subject']}\n" 
                    if task['subject'] != None else "")
        message += (f"Fecha: {task['date']}\n" 
                    if task['date'] != None else "")
        message += ("-" * 42)
    
    return message
