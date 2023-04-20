from .database.mongodatabase import *

def add_users(data):
    """Adds users to the database, making the corresponding validations.
    One user can be associated with multiple chat_id.

    Inputs:
    data -> array [chat_id, username]
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
