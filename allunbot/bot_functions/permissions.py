from .database.mongodatabase import *

def permission_user(username, permission):
    """Adds or updates the permissions of a user.
    
    Inputs:
    username -> string with the user to be changed.
    permission -> string wit the permission to be changed.
    """

    query = {"username": username}
    results = mongo_db["permissions"].count_documents(query)

    if results < 1:
        add_permission_user(username, permission)
    else:
        update_permissions_user(username, permission)


def update_permissions_user(username, permission):
    """Updates the permissions of a user.
    
    Inputs:
    username -> string with the user to be updated.
    permission -> string wit the permission to be updated.

    Returns:
    boolean with the status of the update.
    """

    query = {"username": username}
    results = mongo_db["permissions"].find_one(query)
    try:
        update = {"$set": {
                "permissions": results.append(permission),
            }}
        mongo_db["permissions"].update_one(query, update)
        return True
    except:
        return False


def add_permission_user(username, permission):
    """Adds permission to a user in the database, making the corresponding
    validations.

    Inputs:
    username -> string with the user to be added.
    permission -> string wit the permission to be added.
    """

    permissions = {
            "permissions": [permission],
            "username": username,
        }
    
    mongo_db["permissions"].insert_one(permissions)

def get_permissions_by_user(username):
    """Returns the permissions a given user has.
    
    Inputs:
    username -> string with the user.

    Returns:
    array with the user's permissions.
    """
    
    query = {"username": username}
    projection = {
        "_id": 0,
        "permissions": 1,
    }
    result = mongo_db.permissions.find_one(query, projection)
    len_result = mongo_db.permissions.count_documents(query)

    if len_result == 0:
        return []
    else:
        return result["permissions"]
