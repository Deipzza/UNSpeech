import time

import prettytable as pt
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from .database.manage_database import *

def get_page_academic_history(driver=None):
    if driver != None:

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
        with open("page_source.html","w") as file:
            file.write(pag_academic_history)
    else:
        pag_academic_history = open("page_source.html","r")

    return pag_academic_history

def get_page_schedule(driver):

    try: 
        schedule = driver.find_element(By.XPATH, value="//a[@title='Mi horario']")
    except:
        academic_information = driver.find_element(By.XPATH, value="//td[@title='Información académica']")
        driver.execute_script("arguments[0].click();", academic_information)    
        time.sleep(2)
        
        schedule = driver.find_element(By.XPATH, value="//a[@title='Mi horario']")

    schedule.click()
    time.sleep(5)

    # pag_schedule = driver.page_source
    # with open("page_source.html","w") as file:
    #     file.write(pag_schedule)

    return driver

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