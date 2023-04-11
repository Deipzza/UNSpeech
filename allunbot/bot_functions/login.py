import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions

from database.manage_database import *

db = 'allunbot.db'

def auth(payload) -> webdriver.Chrome:
    """Authenticates the student with its credentials.
    """
    chat_id = payload["chat_id"]
    options = ChromeOptions()
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://sia.unal.edu.co/ServiciosApp")

    user_input = driver.find_element(by=By.XPATH, value="//input[@id='username']")
    password_input = driver.find_element(by=By.XPATH, value="//input[@id='password']")
    login_button = driver.find_element(by=By.XPATH, value="//input[@name='submit']")

    user_input.send_keys(payload["username"])
    password_input.send_keys(payload["password"])

    login_button.click()

    del user_input
    del password_input
    del login_button

    time.sleep(5)
    
    try:
        user_loggen = driver.find_element(by=By.XPATH, value="//a[@class='af_menu_bar-item-text']").text
        login = user_loggen == payload["username"]
    except:
        login = False

    if login:
        add_users([chat_id, payload["username"]])
        return (True, driver)
    else:
        return (False, None)


def create_table_users():
    query = """
        CREATE TABLE users(
            chat_id TEXT PRIMARY KEY,
            username TEXT NOT NULL
        );
        """
    create_table(db,"users",query)

def add_users(data):
    """Añadir un usuario a la base de datos.

    La función toma una arreglo [chat_id, username] y hace las validaciones
    pertinentes para agregarlo.
    Un usuario puede estar asociado a varios chat_id.
    """

    sql = "SELECT * FROM users WHERE chat_id = ?;"
    result = select_data_query(sql, db, [data[0]])

    if len(result) == 0:
        sql="""
            INSERT INTO users VALUES (?, ?)
            """
        insert_values_by_query([data], db, sql)
    elif result[0][1] != data[1]:
        sql="""
            UPDATE users SET username = ? WHERE chat_id = ?
            """
        select_data_query(sql, db, data.reverse())

def get_user_by_chat(chat_id):
    sql = "SELECT username FROM users WHERE chat_id = ?;"
    result = select_data_query(sql, db, [chat_id])

    if len(result) == 0:
        return ""
    else:
        return result[0][0]
    
# create_table_users()