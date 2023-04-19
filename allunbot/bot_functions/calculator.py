import regex
from utils import *

def get_subjects(driver):
    pag_academic_history = get_page_academic_history(driver)
    page_soup = BeautifulSoup(pag_academic_history, 'html5lib')
    table = page_soup.find("div", id = "pt1:r1:1:t17::db").find("table")
    result = process_table_subject(table)

    now_plan = page_soup.find("select", id = "pt1:r1:1:soc1::content").get("title")
    plans = page_soup.find("select", id = "pt1:r1:1:soc1::content").find_all("option")

    for plan in plans:
        plan_text = plan.text
        if plan == now_plan:
            continue
        elif plan_text[5:] == now_plan[5:]:
            print(plan_text)
            pag_academic_history = get_page_academic_history_by_plan(driver, plan.get("value"))
            page_soup = BeautifulSoup(pag_academic_history, 'html5lib')
            table = page_soup.find("div", id = "pt1:r1:1:t17::db").find("table")
            result = process_table_subject(table, result)

    return [now_plan[5:]] + result

def create_table_calculator():
    query = """
        CREATE TABLE calculator(
            username TEXT PRIMARY KEY,
            plan_estudios TEXT NOT NULL, 
            ponderado NUMBER NOT NULL,
            creditos NUMBER NOT NULL,
            suma NUMBER NOT NULL,
            size NUMBER NOT NULL
        );
        """
    create_table(db,"calculator",query)


def add_calculator_user(data):
    sql="""
        INSERT INTO
            calculator
            VALUES (?, ?, ?, ?, ?, ?)
        """
    insert_values_by_query([data], db, sql)


def update_calculator_user(data):
    sql="""
        UPDATE calculator
            SET
            plan_estudios = ?,
            ponderado = ?,
            fund_op = ?,
            creditos = ?,
            suma = ?,
            size = ?
            WHERE username = ?
        """
    username = data[0]
    data = data[1:]
    data.append(username)
    update_data_query(sql, db, data)


def calculator(username, data):
    sql = "SELECT * FROM calculator WHERE username = ?;"
    result = select_data_query(sql, db, [username])

    data = [username] + data

    if len(result) == 0:
        add_calculator_user(data)
    else:
        update_calculator_user(data)

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