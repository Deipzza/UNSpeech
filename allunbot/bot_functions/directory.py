import requests
from bs4 import BeautifulSoup

from .database.manage_database import *

db = "allunbot.db"

def get_directory():
    insert_data, position = [], 2
    base = "https://medellin.unal.edu.co/directoriotelefonico.html"
    URL=base
    
    while(True):
        page_request = requests.get(URL)
        soup = BeautifulSoup(page_request.content, 'html5lib')
        rows = soup.find_all("tr", attrs={"class":"fabrik_row"})

        insert_data += select_data_scrap(rows)
        
        try:
            URL = base + soup.find("a", {"title": position })["href"]
        except TypeError:
            print("No hay más registros")
            break

        position += 1
        
    insert_values(insert_data, db)
    

def create_table_directory():
    sql = """
            CREATE TABLE directorio(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                area NOT NULL,
                dependencia NOT NULL,
                telefono NOT NULL,
                ubicacion NOT NULL,
                correo NOT NULL,
                extension NOT NULL,
                adicionales DEFAULT NULL
            )
          """
    create_table(db, "directorio", sql)

def update_directory():
    create_table_directory()
    get_directory()

def insert_values(insert_data, db):
    sql="""
            INSERT INTO
            directorio(area,dependencia,telefono,ubicacion,correo,extension)
            VALUES (?,?,?,?,?,?)
        """
    insert_values_by_query(insert_data, db, sql)

def select_data_scrap(rows):
    data=[]
    for row in rows:
        cells = row.findAll("td")[:-1]
        cells = list(map(lambda x: x.text.strip(), cells))
        data.append(cells)
    return data

def select_query_directorio(metadata,db):
    
    param, response = ["",""], ""
    operator = "AND" if len(metadata) > 1 else 'OR'

    for word in metadata:
        param[0] += f"area LIKE '%{word}%' OR "
        param[1] += f"dependencia LIKE '%{word}%' OR "

    sql=f"SELECT * FROM directorio WHERE ({param[0][:-4]}) {operator} ({param[1][:-4]})"
    
    consulta = select_data_query(sql,db)
    
    if len(consulta) < 1:
        return "Lo sentimos no hemos encontrado registros."
    
    for fila in consulta:
        response += f"{fila[1]} / {fila[2]}\n"
        response += f"Número de teléfono: {fila[3]}\n"
        
        if fila[4] != "":
            response += f"Ubicación: {fila[4]}\n"
        
        if fila[5] != "":
            response += f"Correo: {fila[5]}\n"
        
        response += "----------------------------------\n"

    return response