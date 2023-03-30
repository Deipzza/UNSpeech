from .database.manage_database import *

db = 'allunbot.db'

def create_table_groups():
    sql = """
            CREATE TABLE grupos(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                codigo INTEGER NOT NULL,
                nombre NOT NULL,
                enlace NOT NULL
            )
          """
    create_table(db, "grupos", sql)

def insert_values_into_groups(subject_code, subject_name, link):
    insert_data = [[subject_code, subject_name, link]]
    
    sql = """
            INSERT INTO
            grupos(codigo, nombre, enlace)
            VALUES (?,?,?)
        """
    insert_values_by_query(insert_data, db, sql)

def select_query_groups(subject_code, db):
    param, response = [""], ""
    param[0] += f"codigo = '{subject_code}'"

    sql = f"SELECT * FROM grupos WHERE ({param[0]})"
    query = select_data_query(sql, db)
    
    if len(query) < 1:
        return "Lo sentimos, no hemos encontrado registros."
    
    for fila in query:
        response += f"Código de la asignatura: {fila[1]}\n"
        response += f"Nombre del grupo: {fila[2]}\n"
        response += f"Enlace de TG del grupo: {fila[3]}\n"
        response += "----------------------------------\n"

    return response
