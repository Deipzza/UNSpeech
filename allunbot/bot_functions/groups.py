from .database.mongodatabase import *

mongo_db = get_database()

def insert_values_into_groups(subject_code, subject_name, link):
    collection = mongo_db["grupos"]

    item = {
        "codigo": subject_code,
        "nombre": subject_name,
        "enlace": link,
    }

    collection.insert_one(item)

def select_query_groups(subject_code):
    response = ""

    # Create query for the search
    query = {
        'codigo': {'$eq': subject_code}
    }
    
    # Select which fields to retrieve from the query
    projection = {
        "_id": 0, 
        "codigo": 1, 
        "nombre": 1,
        "enlace": 1,
    }

    # Run query
    results = mongo_db.grupos.find(query, projection)

    if mongo_db.grupos.count_documents(query) < 1:
        return "Lo siento, no he encontrado registros que coincidan."
    
    for row in results:
        response += f"Código de la asignatura: {row['codigo']}\n"
        response += f"Nombre del grupo: {row['nombre']}\n"
        response += f"Enlace de Telegram del grupo: {row['enlace']}\n"
        response += "----------------------------------\n"

    return response