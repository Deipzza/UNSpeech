import regex
from .utils import *

def get_calculator(driver):
    pag_academic_history = get_page_academic_history(driver)
    page_soup = BeautifulSoup(pag_academic_history, 'html5lib')
    table = page_soup.find("span", {"class":"asignaturas-expediente"}).find("table", {"class": "af_table_data-table"})
    result = process_table_subject(table)

    now_plan = page_soup.find("select", {"class": "af_selectOneChoice_content"}).get("title")
    plans = page_soup.find("select", {"class": "af_selectOneChoice_content"}).find_all("option")

    for plan in plans:
        plan_text = plan.text
        if plan == now_plan:
            continue
        elif plan_text[5:] == now_plan[5:]:
            print(plan_text)
            pag_academic_history = get_page_academic_history_by_plan(driver, plan.get("value"))
            page_soup = BeautifulSoup(pag_academic_history, 'html5lib')
            table = page_soup.find("span", {"class":"asignaturas-expediente"}).find("table", {"class": "af_table_data-table"})
            result = process_table_subject(table, result)

    return [now_plan[5:]] + result

def add_calculator_user(data, username):
    """Inserts the data scraped to the database.

    Inputs:
    db -> database connection.
    data -> data to be inserted.
    """

    # Get or create collection
    collection = mongo_db["calculator"]

    # Organize and insert the data
    document = {
        'username': username, 
        'plan_estudios': data[0],
        'ponderado': data[1],
        'creditos': data[2],
        'suma': data[3],
        'size': data[4]
    }
    collection.insert_one(document)


def update_calculator_user(data, username):
    """Updates the academic history for a user.

    Inputs:
    db -> database connection.
    data -> data to be updated.
    """

    collection = mongo_db["grades"]

    query = {"username": username}
    update = {"$set": {
        'plan_estudios': data[0],
        'ponderado': data[1],        
        'creditos': data[2],
        'suma': data[3],
        'size': data[4]
    }}
    collection.update_one(query, update)


def calculator(username, data):
    """Adds or updates the academic history of a user.

    Inputs:
    username -> string of the student's username.
    data -> data to be added or updated.
    """
    query = {"username": username}
    results = mongo_db.calculator.count_documents(query)

    if results == 0:
        add_calculator_user(data, username)
    else:
        update_calculator_user(data, username)

#-----------------------------------------
def process_table_subject(table, values = [0, 0, 0, 0]):
    
    content = table.find("tbody")
    ponderado, creditos, suma, size = values


    for row in content.find_all("tr"):
        cells = row.findAll("td")

        if len(cells) > 2:
            credito = int(cells[1].find("span").text)
            nota = cells[4].find("span").text
            nota = regex.sub(r"(APROBADA)|(REPROBADA)", "", nota)

            if nota == "" or not isfloat(nota):
                continue
            
            nota = float(nota)
            ponderado += nota * credito
            creditos += credito
            suma += nota
            size += 1


    return [round(ponderado,2) , creditos, round(suma, 2), size]