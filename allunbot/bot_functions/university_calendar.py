import requests
from bs4 import BeautifulSoup
from .database.manage_database import *
from .database.mongodatabase import *

# Database
db = 'allunbot.db'
# mongo_db = get_database()

def get_academic_calendar(student):
    """Scraps the academic calendar for the type of student received.

    Inputs:
    student -> string with the type of the student.

    Returns:
    Information formated.
    """

    print("Started retrieving data") # Log print

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
            # print("1", anchor)
            if (("CALENDARIO ACADÉMICO 2023-1S" in anchor) and (f"{student.upper()}" in anchor)):
                URL = collapse.find("div").find("a")["href"]
                # print(2, URL)
                page_request = requests.get(URL)
                soup = BeautifulSoup(page_request.content, 'html5lib')
                scrapTable = True

                if ("MODIFICACIÓN" in anchor):
                    # print(3)
                    scrapTable = False
                    modif = soup.find_all("span")

                    for span in modif:
                        # print(4)
                        if ("calendario del periodo académico 2023-1S" in span.text):
                            # print(5)
                            scrapTable = True
                            break

                if (scrapTable):
                    # print(6)
                    table = soup.find_all("table", attrs = {"class": "MsoNormalTable"})
                    # print("aaa")
                    # result = process_table(table[0], [0, 1], student)
                    result = process_table("a", "b", "c")
                    # print("result", result)
                    return result
        except:
            # print(7)
            pass

    # print("Finalized retrieving data") # Log print
    # print(result)
    return result

# get_academic_calendar("pregrado")

def get_request_calendar(student):
    """Scraps the request calendar for the type of student received.

    Inputs:
    student -> string with the type of the student.

    Returns:
    Information formated.
    """

    # print("Started retrieving data") # Log print

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
            if (("CALENDARIO ACADÉMICO 2023-1S" in anchor) and (f"{student.upper()}" in anchor) and "MODIFICACIÓN" not in anchor):
                URL = collapse.find("div").find("a")["href"]
                page_request = requests.get(URL)
                soup = BeautifulSoup(page_request.content, 'html5lib')
                table = soup.find_all("table", attrs = {"class": "MsoNormalTable"})
                result = process_table(table[1], [1, 2], student)

                return result
        except:
            pass

    # print("Finalized retrieving data") # Log print
    
    return result
    # insert_values(mongo_db, result)

def insert_values(db, data):
    """Inserts the info into the database.

    Inputs:
    db -> database.
    data -> information to get inserted.
    """
    # Get or create collection
    collection = db["calendario_academico"]

    # Organize and insert the data
    for sublist in data:
        document = {
            'indice': sublist[0], 
            'actividad': sublist[1], 
            'fecha': sublist[2],
            'tipo_estudiante': sublist[3],
        }
        collection.insert_one(document)

    print("Finalized inserting data") # Log print

def update_academic_calendar():
    """Updates the academic calendar in case it changed."""

    # Creation query
    query = """
            CREATE TABLE academic_calendar(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                indice INTEGER NOT NULL,
                actividad TEXT NOT NULL,
                fecha TEXT(20) NOT NULL,
                tipo_estudiante TEXT(20) NOT NULL
            );
            """
    create_table(db, "academic_calendar", query)

    students = ["pregrado", "posgrado"]

    for student in students:
        insert_data = get_academic_calendar(student)
        sql = """
            INSERT INTO
                academic_calendar(indice, actividad, fecha, tipo_estudiante)
                VALUES (?, ?, ?, ?)
            """
        insert_values_by_query(insert_data, db, sql)

# def update_academic_calendar():
#     """Updates the academic calendar in case it changed."""
#     reset_collection(mongo_db, "calendario_academico")

#     students = ["pregrado","posgrado"]

#     for student in students:
#         get_academic_calendar(student)

def update_request_calendar():
    """Updates the request calendar in case it changed."""

    # Creation query
    query = """
            CREATE TABLE request_calendar(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                indice INTEGER NOT NULL,
                actividad TEXT NOT NULL,
                fecha TEXT(20) NOT NULL,
                tipo_estudiante TEXT(20) NOT NULL
            );
            """
    create_table(db, "request_calendar", query)

    students = ["pregrado", "posgrado"]

    for student in students:
        insert_data = get_request_calendar(student)
        sql="""
            INSERT INTO
                request_calendar(indice, actividad, fecha, tipo_estudiante)
                VALUES (?, ?, ?, ?)
            """
        insert_values_by_query(insert_data, db, sql)

def process_table(table, positions, student):
    """Formats the tables for a better handling.

    Inputs:
    table -> information to be formated.
    positions -> 
    student -> type of student.
    """

    # print(8)
    content = table.find("tbody")
    result = []
    count = 0

    for row in content.find_all("tr"):
        print(9)
        cells = row.findAll("td")

        if len(cells) > 2:
            print(10)
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
    sql = """
            SELECT * 
            FROM academic_calendar
            WHERE tipo_estudiante = ?
          """
    response = select_data_query(sql, db, (student,))
    message = ""
    
    # Formatting the data retrieved
    for item in response:
        message += f"{item[1]} | {item[2]} | {item[3]}.\n\n"

    return message

def generate_request_calendar(student):
    """Returns the request calendar as a message.

    Inputs:
    student -> string with the student type.

    Returns:
    A string with the request calendar in message format.
    """

    # Query for getting the data
    sql = """
            SELECT * 
            FROM request_calendar
            WHERE tipo_estudiante = ?
          """
    response = select_data_query(sql, db, (student,))
    message = ""
    
    # Formatting the data retrieved
    for item in response:
        if len(item[3]) < 5:
            message += f"**{item[1]}. {item[2]}** \n\n"    
            continue
        message += f"{item[1]} | {item[2]} | {item[3]}.\n\n"

    return message
