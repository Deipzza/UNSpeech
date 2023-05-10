import requests

from bs4 import BeautifulSoup

from .database.mongodatabase import *

def get_directory():
    """Extracts the data from the university's directory."""

    insert_data, position = [], 2
    base = "https://medellin.unal.edu.co/directoriotelefonico.html"
    URL = base

    # Scraping process.
    while(True):
        page_request = requests.get(URL)
        soup = BeautifulSoup(page_request.content, 'html5lib')
        rows = soup.find_all("tr", attrs = {"class": "fabrik_row"})

        insert_data += select_data_scrap(rows)
        
        try:
            URL = base + soup.find("a", {"title": position})["href"]
        except TypeError:
            break

        position += 1

    insert_values(insert_data)


def update_directory():
    """Control function to update the directory in case it changes."""

    reset_collection("directory")
    get_directory()


def insert_values(data):
    """Insert the values extracted from the directory's page into the
    database.
    
    Inputs:
    data -> array with the data scraped.
    """

    # Get or create collection
    collection = mongo_db["directory"]

    # Organize and insert the data
    for sublist in data:
        document = {
            'area': sublist[0], 
            'dependencia': sublist[1], 
            'telefono': sublist[2],
            'unicacion': sublist[3],
            'correo': sublist[4],
            'extension': sublist[5],
        }
        collection.insert_one(document)


def select_data_scrap(rows):
    """Selects the actual data to work with from the scraped information.
    
    Inputs:
    rows -> list of the elements from the scraped data.

    Returns:
    array with the data.
    """

    data = []

    for row in rows:
        cells = row.findAll("td")[:-1]
        cells = list(map(lambda x: x.text.strip(), cells))
        data.append(cells)

    return data


def select_query_directory(metadata):
    """Makes a query to the database to select the directory collection.
    
    Inputs:
    metadata -> array with the words written by the user.

    Returns:
    string with the information formatted.
    """

    response = ""

    # Create query for the search
    query = {
        '$and': [
            {'$or': [{'dependencia': {'$regex': word, '$options': 'i'}} for word
                     in metadata]},
            {'$or': [{'area': {'$regex': word, '$options': 'i'}} for word
                     in metadata]},
        ]
    }

    # Select which fields to retrieve from the query
    projection = {
        "_id": 0, 
        "area": 1, 
        "dependencia": 1,
        "telefono": 1,
        "ubicacion": 1,
        "correo": 1,
        "extension": 1,
    }

    # Run query
    results = mongo_db.directory.find(query, projection)

    if mongo_db.directory.count_documents(query) < 1:
        return "Lo siento, no he encontrado registros que coincidan."
    
    # Format the results
    for row in results:
        response += f"{row['area']} / {row['dependencia']}\n"
        response += f"Número de teléfono: {row['telefono']} - Ext: {row['extension']}\n"
        
        if 'ubicacion' in row:
            response += f"Ubicación: {row['ubicacion']}\n"
        
        if 'correo' in row:
            response += f"Correo: {row['correo']}\n"
        
        response += "-" * 34 + "\n"
    
    return response
