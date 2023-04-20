import time

from bs4 import BeautifulSoup
import prettytable as pt
from selenium.webdriver.common.by import By

from .database.mongodatabase import *

def get_page_academic_history(driver = None):
    """
    """

    try: 
        academic_history = driver.find_element(By.XPATH, value="//a[@title='Mi historia académica']")
    except:
        academic_information = driver.find_element(By.XPATH, value="//td[@title='Información académica']")
        driver.execute_script("arguments[0].click();", academic_information)    
        time.sleep(2)
        
        academic_history = driver.find_element(By.XPATH, value="//a[@title='Mi historia académica']")

    academic_history.click()
    time.sleep(6)

    pag_academic_history = driver.page_source

    return pag_academic_history

def get_page_schedule(driver):
    """
    """

    try: 
        schedule = driver.find_element(By.XPATH, value = "//a[@title='Mi horario']")
    except:
        academic_information = driver.find_element(By.XPATH, value = "//td[@title='Información académica']")
        driver.execute_script("arguments[0].click();", academic_information)    
        time.sleep(2)
        
        schedule = driver.find_element(By.XPATH, value = "//a[@title='Mi horario']")

    schedule.click()
    time.sleep(5)

    return driver

def get_page_academic_history_by_plan(driver, id):
    """
    """

    td = driver.find_element(By.XPATH, value = "//td[@class='AFContentCell']") 
    select = driver.find_element(By.XPATH, value = ".//select[@class='af_selectOneChoice_content']") 
    option = driver.find_element(By.XPATH, value = f".//option[@value={id}]")
    option.click()
    time.sleep(5)

    pag_academic_history = driver.page_source

    return pag_academic_history

def get_page_grades(driver):
    """
    """

    try: 
        my_grades = driver.find_element(By.XPATH, value = "//a[@title='Mis Calificaciones']")
    except:
        academic_information = driver.find_element(By.XPATH, value = "//td[@title='Información académica']")
        driver.execute_script("arguments[0].click();", academic_information)    
        time.sleep(2)
        
        my_grades = driver.find_element(By.XPATH, value = "//a[@title='Mis Calificaciones']")

    my_grades.click()
    time.sleep(6)

    return driver

def isfloat(value):
    """Check if grades are float type."""

    try:
        float(value)
        return True
    except ValueError:
        return False

def process_table(table):
    """
    """
    
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
