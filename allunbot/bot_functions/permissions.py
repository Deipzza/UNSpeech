from .database.mongodatabase import *


def permission_user(username, permission):
    query = {"username": username}
    results = mongo_db["permissions"].count_documents(query)

    if results < 1:
        add_permission_user(username, permission)
    else:
        update_permissions_user(username, permission)


def update_permissions_user(username, permission):
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
    """Adds permission to user to the database, making the corresponding validations.
    """

    permissions = {
            "permissions": [permission],
            "username": username,
        }
    
    mongo_db["permissions"].insert_one(permissions)

def get_permissions_by_user(username):

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

