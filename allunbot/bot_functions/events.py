from bson import ObjectId
import datetime
import locale

from .database.mongodatabase import *

# Set the locale to Spanish and Colombian locale
locale.setlocale(locale.LC_ALL, 'es_CO.utf8')

def add_event(data):
    """Inserts a event into the database with the given fields.

    Inputs:
    data -> event object with the corresponding fields

    Returns:
    boolean indicating if the event was inserted
    """

    # Get or create collection
    collection = mongo_db["events"]

    # Organize and insert the data
    item = {
        "username": verify_field_null(data["username"]),
        "name": verify_field_null(data["name"]),
        "description": verify_field_null(data["description"]),
        "url": verify_field_null(data["url"]),
        "dependency": verify_field_null(data["dependency"]),
        "status": verify_field_null(data["status"]),
        "date": verify_field_null(data["date"]),
        "start-time": verify_field_null(data["start-time"]),
        "final-time": verify_field_null(data["final-time"])
    }
    
    try:
        collection.insert_one(item)
        return True
    except:
        return False


def update_event(id, data):
    """Updates the event of the given ID.

    Inputs:
    data -> data to be updated.
    id -> id of the event to be updated.
    """

    collection = mongo_db["events"]

    query = {"_id": ObjectId(id)}
    update = {
        "$set": {
            "username": verify_field_null(data["username"]),
            "name": verify_field_null(data["name"]),
            "description": verify_field_null(data["description"]),
            "url": verify_field_null(data["url"]),
            "dependency": verify_field_null(data["dependency"]),
            "status": verify_field_null(data["status"]),
            "date": verify_field_null(data["date"]),
            "start-time": verify_field_null(data["start-time"]),
            "final-time": verify_field_null(data["final-time"])
        }
    }

    try:
        collection.update_one(query, update)
        return True
    except:
        return False
    

def remove_event(id):
    """Removes the event of the given ID.

    Inputs:
    id -> id of the event to be removed.
    """

    collection = mongo_db["events"]
    query = {"_id": ObjectId(id)}

    try:
        collection.delete_one(query)
        return True
    except:
        return False


def verify_field_null(field):
    """Verifies that a field is an empty string or undefined, in which case
    returns None.
    
    Inputs:
    field -> the field to be checked.

    Returns:
    the field if it's not an empty string or undefined; None otherwise.
    """

    if field == "" or field == "undefined":
        return None
    return field


def event(data):
    """Checks if the event is going to be added or updated
    depending on the ID.

    Inputs:
    id -> string with the event identifier.
    data -> dict with the event data.

    Returns:
    boolean that indicates whether the event could be added or updated.
    """
    return add_event(data)


def select_query_events(query):
    """Retrieves the list of events for a given username.

    Inputs:
    username -> string

    Returns:
    The list of events in message format.
    """

    # Select which fields to retrieve from the query
    projection = {
        "_id": 1, 
        "username": 1,
        "name": 1,
        "description": 1,
        "url": 1,
        "dependency": 1,
        "status": 1,
        "date": 1,
        "start-time": 1,
        "final-time": 1
    }

    results = mongo_db.events.find(query, projection) # Run query

    return results


def get_events_by_user(username):
    """Returns the events of a user parsed."""

    return parse_event_list(select_query_events({"username": username}))


def get_events():
    """Returns all of the events parsed."""

    return parse_event_list(select_query_events({}))


def get_today_events():
    """Returns a list of the events that occur the day of the query."""

    today = str(datetime.date.today())

    # Create query for the search
    query = {
        "$and": [
            {"date": {"$regex": f"^{today}"}}
        ]
    }

    results = select_query_events(query) # Make the search
    event_list = parse_event_list(results) # Format the results

    return event_list


def parse_event_list(event_list):
    """Format the list of events to fill the blank fields.

    Inputs:
    event_list -> MongoDB cursor object with the results of the query.
    Returns:
    list of dictionaries with the events.
    """

    formated_list = []

    for event in event_list:
        event["description"] = (
            "" if "description" not in event else event["description"]
        )
        event["url"] = (
            "" if "url" not in event else event["url"]
        )
        event["dependency"] = (
            "" if "dependency" not in event else event["dependency"]
        )
        event["start-time"] = (
            "" if "start-time" not in event else event["start-time"]
        )
        event["final-time"] = (
            "" if "final-time" not in event else event["final-time"]
        )
        formated_list.append(event)

    return formated_list


def get_message_today_events():
    """Returns the list of today's events formatted as a message."""

    message = "*Eventos de hoy.*"
    events = get_today_events()

    for event in events:
        message += f"\nNombre: {event['name']}\n"
        message += f"Dependencia: {event['dependency']}\n"
        message += f"Fecha: {event['date']}\n"
        message += f"Estado: {event['status']}\n"
        message += (f"Descripción: {event['description']}\n" 
                    if event['description'] else "")
        message += (f"Hora inicio: {event['start-time']}\n" 
                    if event['start-time'] else "")
        message += (f"Hora fin: {event['final-time']}\n" 
                    if event['final-time'] else "")
        message += (f"Más información: {event['url']}\n" 
                    if event['url'] else "")
        message += "-" * 32
    
    return message
