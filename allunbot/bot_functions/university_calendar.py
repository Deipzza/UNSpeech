import requests
from bs4 import BeautifulSoup
from .database.manage_database import *

db="allunbot.db"

def get_academic_calendar(student):
    URL = "https://minas.medellin.unal.edu.co/tramitesestudiantiles/calendarios/calendario-academico-sede-medellin.html"
    page_request = requests.get(URL)
    soup = BeautifulSoup(page_request.content, 'html5lib')
    collapses = soup.find_all("li")
    result = "Lo siento. No he podido encontrar esa información."

    for collapse in collapses:
        try:
            anchor = collapse.find("a").text
            if (("CALENDARIO ACADÉMICO 2023-1S" in anchor) and (f"{student.upper()}" in anchor)):
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
                    result = process_table(table[0], [0, 1], student)
                    return result
        except:
            pass

    return result

def get_request_calendar(student):
    URL = "https://minas.medellin.unal.edu.co/tramitesestudiantiles/calendarios/calendario-academico-sede-medellin.html"
    page_request = requests.get(URL)
    soup = BeautifulSoup(page_request.content, 'html5lib')
    collapses = soup.find_all("li")
    result = "Lo sentimos. No hemos podido encontrar esa información."

    for collapse in collapses:
        try:
            anchor = collapse.find("a").text
            if (("CALENDARIO ACADÉMICO 2023-1S" in anchor) and (f"{student.upper()}" in anchor) and "MODIFICACIÓN" not in anchor):
                URL = collapse.find("div").find("a")["href"]
                page_request = requests.get(URL)
                soup = BeautifulSoup(page_request.content, 'html5lib')
                table = soup.find_all("table", attrs = {"class": "MsoNormalTable"})
                result = process_table(table[1], [1,2], student)
                return result
        except:
            pass

    return result

def update_academic_calendar():
    
    query = """
            CREATE TABLE academic_calendar(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                indice INTEGER NOT NULL,
                actividad TEXT NOT NULL,
                fecha TEXT(20) NOT NULL,
                tipo_estudiante TEXT(20) NOT NULL
            );
            """
    create_table(db,"academic_calendar",query)

    students = ["pregrado","posgrado"]
    for student in students:
        insert_data = get_academic_calendar(student)
        sql="""
            INSERT INTO
                academic_calendar(indice, actividad, fecha, tipo_estudiante)
                VALUES (?, ?, ?, ?)
            """
        insert_values_by_query(insert_data,db,sql)

def update_request_calendar():
    
    query = """
            CREATE TABLE request_calendar(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                indice INTEGER NOT NULL,
                actividad TEXT NOT NULL,
                fecha TEXT(20) NOT NULL,
                tipo_estudiante TEXT(20) NOT NULL
            );
            """
    create_table(db,"request_calendar",query)

    students = ["pregrado","posgrado"]
    for student in students:
        insert_data = get_request_calendar(student)
        sql="""
            INSERT INTO
                request_calendar(indice, actividad, fecha, tipo_estudiante)
                VALUES (?, ?, ?, ?)
            """
        insert_values_by_query(insert_data,db,sql)

def process_table(table, positions,student):
    
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
    
    sql = """
            SELECT * 
            FROM academic_calendar
            WHERE tipo_estudiante = ?
          """
    response = select_data_query(sql, db, (student,))
    message = ""
    
    for item in response:
        message += f"{item[1]} | {item[2]} | {item[3]}.\n\n"

    return message

def generate_request_calendar(student):
    
    sql = """
            SELECT * 
            FROM request_calendar
            WHERE tipo_estudiante = ?
          """
    response = select_data_query(sql, db, (student,))
    message = ""
    
    for item in response:
        if len(item[3]) < 5:
            message += f"**{item[1]}. {item[2]}** \n\n"    
            continue
        message += f"{item[1]} | {item[2]} | {item[3]}.\n\n"

    return message
