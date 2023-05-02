from bson import ObjectId

from .database.mongodatabase import *


def permission_user(username, permission):
    query = {"username": username}
    results = mongo_db.grades.count_documents(query)

    if results < 1:
        add_grades_user(data, username)
    else:
        update_permissions_user(username, permission)


def update_permissions_user(username, permission):
    query = {"username": username}
    results = mongo_db.grades.find_one(query)
    

def add_permission_user(username, permission):
    """Adds permission to user to the database, making the corresponding validations.
    """

    query = {"chat_id": data[0]}
    projection = {
        "_id": 0,
        "chat_id": 1,
        "username": 1,
    }
    collection = mongo_db["users"]
    result = collection.find_one(query, projection)
    len_result = collection.count_documents(query)

    if len_result == 0: # If the user is not registered
        user = {
            "chat_id": data[0],
            "username": data[1],
        }
        collection.insert_one(user)
    elif result["username"] != data[1]: # If the chat_id has another username
        update = {"$set": {
            "username": data[1],
        }}
        collection.update_one(query, update)

def get_user_by_chat(chat_id):
    """Searches a user by a given chat_id.

    Inputs:
    chat_id -> string with the user's chat ID.

    Returns:
    string with the user's name.
    """

    query = {"chat_id": str(chat_id)}
    projection = {
        "_id": 0,
        "username": 1,
    }
    result = mongo_db.users.find_one(query, projection)
    len_result = mongo_db.users.count_documents(query)

    if len_result == 0:
        return ""
    else:
        return result["username"]

def get_users():
    """Returns a list of all user's chat IDs."""

    projection = {
        "_id": 0,
        "username": 1,
        "chat_id": 1,
    }
    result = mongo_db.users.find({}, projection)
    
    return list(result)
