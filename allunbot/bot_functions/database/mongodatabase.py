from pymongo import MongoClient
from dotenv import load_dotenv
import os

def get_database():
    """Creates a connection to the database.

    Returns:
    Database object.
    """

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    load_dotenv(os.path.join(BASE_DIR, '.env'))
    connection_string = os.environ.get("CONNECTION_STRING")

    # Connection to the database
    client = MongoClient(connection_string)

    # Assign the connection to the database
    db = client['allunbot']

    return db

def reset_collection(collection_name):
    """Deletes all documents of the collection.

    Inputs:
    db -> Database object.
    collection_name -> Collection to be cleared.
    """

    collection = mongo_db[f"{collection_name}"]
    collection.delete_many({})

mongo_db = get_database()