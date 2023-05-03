import os
import time
import requests

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

from .users import *

from .models import User



BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db = os.path.join(BASE_DIR, 'allunbot.db')

def auth(payload):
    """Authenticates the student with its credentials.
    Inputs:
    payload -> dictionary with user's credentials.
    Returns:
    boolean and Selenium driver object.
    """

    chat_id = payload["chat_id"]
    options = ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
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


def request_auth(username, password):
    load_dotenv(os.path.join(BASE_DIR, 'allunbot/.env'))
    URL = os.environ.get("CONNECTION_LDAP")

    payload = {'username': username, 'password': password}

    response = requests.post(URL, json = payload).json()
    return response

def auth_ldap(username, password):
    """Authenticates the student with its credentials."""

    response = request_auth(username, password)

    if "token" in response and response["token"]:
        mongo_db["user_logged"].insert_one({"username":username, "data": response})
        return User(username = username, data = response)

    return None

def load_user(username):
    response = mongo_db["user_logged"].find_one({"username":username})
    
    if response["user"]["uid"] == username:
        return User(username = username, data = response["data"])

    return None