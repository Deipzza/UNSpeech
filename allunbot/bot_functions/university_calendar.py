import requests

from bs4 import BeautifulSoup

from .database.mongodatabase import *

def get_academic_calendar(student):
    """Scraps the academic calendar for the type of student received.

    Inputs:
    student -> string with the type of the student.

    Returns:
    Information formated.
    """

    # Start connection to URL
    URL = "https://minas.medellin.unal.edu.co/tramitesestudiantiles/calendarios/calendario-academico-sede-medellin.html"
    page_request = requests.get(URL)
    soup = BeautifulSoup(page_request.content, 'html5lib')
    collapses = soup.find_all("li")
    result = "Lo siento. No he podido encontrar esa información."

    # Searches the table and stores it if found.
    for collapse in collapses:
        try:
            anchor = collapse.find("a").text
            if (
                ("CALENDARIO ACADÉMICO 2023-1S" in anchor)
                and (f"{student.upper()}" in anchor)
            ):
                URL = collapse.find("div").find("a")["href"]
                page_request = requests.get(URL)
                soup = BeautifulSoup(page_request.content, 'html5lib')
                scrapTable = True

                if ("MODIFICACIÓN" in anchor):
                    scrapTable = False
                    modif = soup.find_all("span")

                    for span in modif:
                        if ("calendario del periodo académico 2023-1S" in span.text):
                            scrapTable = True
                            break

                if (scrapTable):
                    table = soup.find_all("table", attrs = {"class": "MsoNormalTable"})
                    result = process_calendar_table(table[0], [0, 1], student)
                    
                    insert_values(result, "academic_calendar")
        except:
            pass

    return result


def get_request_calendar(student):
    """Scraps the request calendar for the type of student received.

    Inputs:
    student -> string with the type of the student.

    Returns:
    Information formated.
    """

    # Start connection to URL
    URL = "https://minas.medellin.unal.edu.co/tramitesestudiantiles/calendarios/calendario-academico-sede-medellin.html"
    page_request = requests.get(URL)
    soup = BeautifulSoup(page_request.content, 'html5lib')
    collapses = soup.find_all("li")
    result = "Lo sentimos. No hemos podido encontrar esa información."

    # Searches the table and stores it if found.
    for collapse in collapses:
        try:
            anchor = collapse.find("a").text
            if (("CALENDARIO ACADÉMICO 2023-1S" in anchor)
                and (f"{student.upper()}" in anchor)
                and "MODIFICACIÓN" not in anchor):

                URL = collapse.find("div").find("a")["href"]
                page_request = requests.get(URL)
                soup = BeautifulSoup(page_request.content, 'html5lib')
                table = soup.find_all("table", attrs = {
                    "class": "MsoNormalTable"
                })
                result = process_calendar_table(table[1], [1, 2], student)

                insert_values(result, "request_calendar")
        except:
            pass

    return result


def insert_values(data, collection_name):
    """Inserts the info into the database.

    Inputs:
    db -> database.
    data -> information to get inserted.
    """

    # Get or create collection
    collection = mongo_db[collection_name]

    # Organize and insert the data
    for sublist in data:
        document = {
            'indice': sublist[0], 
            'actividad': sublist[1], 
            'fecha': sublist[2],
            'tipo_estudiante': sublist[3],
        }
        collection.insert_one(document)


def update_academic_calendar():
    """Updates the academic calendar in case it changed."""

    reset_collection("academic_calendar")
    students = ["pregrado", "posgrado"]

    for student in students:
        get_academic_calendar(student)


def update_request_calendar():
    """Updates the requests calendar in case it changed."""

    reset_collection("request_calendar")
    students = ["pregrado", "posgrado"]

    for student in students:
        get_request_calendar(student)


def process_calendar_table(table, positions, student):
    """Formats the tables for better handling.

    Inputs:
    table -> information to be formated.
    positions -> 
    student -> type of student.

    Returns:
    formated table
    """

    content = table.find("tbody")
    result = []
    count = 0

    for row in content.find_all("tr"):
        cells = row.findAll("td")

        if len(cells) > 2:
            activity = cells[positions[0]].find("p").text
            date = cells[positions[1]].find("p").text

            result.append((count, activity, date, student))

            count += 1

    return result


def generate_academic_calendar(student):
    """Returns the academic calendar as a message.

    Inputs:
    student -> string with the student type.

    Returns:
    A string with the academic calendar in message format.
    """

    # Query for getting the data
    query = {"tipo_estudiante": student}
    # Select which fields to retrieve from the query
    projection = {
        "_id": 0, 
        "indice": 1,
        "actividad": 1,
        "fecha": 1,
    }
    response = mongo_db.academic_calendar.find(query, projection)
    message = ""
    
    # Formatting the data retrieved
    for item in response:
        message += f"{item['indice']} | {item['actividad']} | {item['fecha']}.\n\n"

    return message


def generate_request_calendar(student):
    """Returns the request calendar as a message.

    Inputs:
    student -> string with the student type.

    Returns:
    A string with the request calendar in message format.
    """

    # Query for getting the data
    query = {"tipo_estudiante": student}
    # Select which fields to retrieve from the query
    projection = {
        "_id": 0, 
        "indice": 1,
        "actividad": 1,
        "fecha": 1,
    }
    response = mongo_db.request_calendar.find(query, projection)
    message = ""
    
    # Formatting the data retrieved
    for item in response:
        if len(item["fecha"]) < 5:
            message += f"**{item['indice']}. {item['actividad']}** \n\n"    
            continue
        message += f"{item['indice']} | {item['actividad']} | {item['fecha']}.\n\n"

    return message
