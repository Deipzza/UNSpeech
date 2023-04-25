import datetime
import locale

from .database.mongodatabase import *

# Set the locale to French
locale.setlocale(locale.LC_ALL, 'es_CO.utf8')

def insert_values_into_tasks(username, name = None, description = None,
                             date = None, notification_time = None, subject = None):
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
        "date": date,
        "notification_time": notification_time,
        "subject": subject,
    }

    collection.insert_one(item)
    return item

def select_query_tasks(username):
    """Retrieves the list of tasks for a given username.

    Inputs:
    username -> string

    Returns:
    The list of tasks in message format.
    """

    response = "Tareas.\n"

    # Create query for the search
    query = {
        'username': {'$eq': username}
    }
    
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
        return "No tienes tareas guardadas."

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

# print(select_query_tasks("dperezz"))