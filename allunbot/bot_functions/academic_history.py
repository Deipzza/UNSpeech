import time
import pandas as pd
import prettytable as pt

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions

from database.manage_database import *
from login import *

db = 'allunbot.db'

def get_academic_history(driver = None):
    if driver != None:
        academic_information = driver.find_element(By.XPATH, value="//td[@title='Información académica']")
        driver.execute_script("arguments[0].click();", academic_information)    
        time.sleep(2)

        academic_history = driver.find_element(By.XPATH, value="//a[@title='Mi historia académica']")
        academic_history.click()
        time.sleep(5)

        pag_academic_history = driver.page_source
        with open("page_source.html","w") as file:
            file.write(pag_academic_history)
    else:
        pag_academic_history = open("page_source.html","r")
    
    page_soup = BeautifulSoup(pag_academic_history, 'html5lib')
    # papa = page_soup.find("span",{"class":"promedios-valor"}).text
    table = page_soup.find("div", id = "pt1:r1:1:t10::db").find("table")
    result = process_table(table)
    return result

def create_table_academic_history():
    query = """
        CREATE TABLE academic_history(
            username TEXT PRIMARY KEY, 
            disc_op TEXT NOT NULL,
            dis_ob TEXT NOT NULL,
            pendientes TEXT NOT NULL,
            inscritos TEXT NOT NULL,
            cursados TEXT NOT NULL
        );
        """
    create_table(db,"academic_history",query)


def add_academic_history_user(data):
    sql="""
        INSERT INTO
            academic_history
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
    insert_values_by_query(data, db, sql)


def update_academic_history_user(data):
    sql="""
        UPDATE academic_history
            SET
            exigidos = ?,
            aprobados = ?,
            pendientes = ?,
            inscritos = ?,
            cursados = ?
            WHERE username = ?
        """
    insert_values_by_query(data,db,sql)


def academic_history(username, data):
    sql = "SELECT * FROM academic_history WHERE username = ?;"
    result = select_data_query(sql, db, [username])
    
    data = pd.DataFrame(data[0])
    data = data.transpose()
    data = [["username", "-".join(data[0]), "-".join(data[1]), "-".join(data[2]), "-".join(data[3]), "-".join(data[4]), "-".join(data[5])]]

    if len(result) == 0:
        add_academic_history_user(data)
    else:
        update_academic_history_user(data)


def generete_academic_history_user(username):
    sql = "SELECT * FROM academic_history WHERE username = ?;"
    result = select_data_query(sql, db,[username])

    if len(result) == 0:
        return result
    else:
        table = pt.PrettyTable(['','Exigidos', 'Aprobados', 'Pendientes', 'Inscritos', 'cursados'])
        tipo = [
            "DISCIPLINAR OPTATIVA", "FUND. OBLIGATORIA", "FUND. OPTATIVA", 
            "DISCIPLINAR OBLIGATORIA", "LIBRE ELECCIÓN","TRABAJO DE GRADO",
            "TOTAL", "NIVELACIÓN", "TOTAL ESTUDIANTE"
        ]

        for i in range(len(result[0])):
            print(result[i])

        # update_academic_history_user(data)

#--------------------------

def process_table(table):
    
    content = table.find("tbody")
    result = []

    for row in content.find_all("tr"):
        cells = row.findAll("td")

        data_row = []

        if len(cells) > 2:
            for cell in cells:
                data_row.append(cell.find("span").text)

            result.append(data_row)

    return result

payload = {"username":"cpatinore","password":"Abril2026"}
driver = login(payload)
data = get_academic_history(driver)
create_table_academic_history()
academic_history(payload["username"], data)
print(generete_academic_history_user(payload["username"]))