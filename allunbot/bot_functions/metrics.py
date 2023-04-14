import os

from .utils import *

db = 'allunbot.db'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
temp = os.path.join(BASE_DIR, 'bot_functions/temp')

def get_metrics(driver=None):
    pag_academic_history = get_page_academic_history(driver)
    page_soup = BeautifulSoup(pag_academic_history, 'html5lib')
    metrics = page_soup.find("span",{"class":"promedios"}).find_all("span",{"class":"promedio-general"})

    result = ["","", ""]
    for metric in metrics:
        tipo = metric.find("span", {"class":"promedios-texto"}).text
        valor = metric.find("span", {"class":"promedios-valor"}).text

        if "P.A.P.A" in tipo:
            result[0] = valor
        else:
            result[1] = valor
    result[2] = page_soup.find("span", id = "pt1:r1:2:i12:0:pgl42").text
        
    return result



def create_table_metrics():
    query = """
        CREATE TABLE metrics(
            username TEXT PRIMARY KEY, 
            papa TEXT NOT NULL,
            promedio TEXT NOT NULL,
            avance TEXT NOT NULL
        );
        """
    create_table(db,"metrics",query)


def add_metrics_user(data):
    sql="""
        INSERT INTO
            metrics
            VALUES (?, ?, ?, ?)
        """
    insert_values_by_query([data], db, sql)


def update_metrics_user(data):
    sql="""
        UPDATE metrics
            SET
            papa = ?,
            promedio = ?,
            avance = ?
            WHERE username = ?
        """
    
    username = data[0]
    data = data[1:]
    data.append(username)
    update_data_query(sql, db, data)


def metrics(username, data):
    sql = "SELECT * FROM metrics WHERE username = ?;"
    result = select_data_query(sql, db, [username])

    if len(result) == 0:
        data = [username] + data
        add_metrics_user(data)
    else:
        data = data + [username]
        update_metrics_user(data)


def generate_metrics_user(username):
    sql = "SELECT * FROM metrics WHERE username = ?"
    result = select_data_query(sql, db, [username])

    if len(result) == 0:
        return False
    else:
        table = pt.PrettyTable(['P.A.P.A', 'Promedio'])
        data = [result[0][1:]]
        table.add_rows(data)
    
    return table


# create_table_metrics()