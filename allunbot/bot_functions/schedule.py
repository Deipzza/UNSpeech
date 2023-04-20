import os
import time

from .utils import *
from .login import *

from .database.mongodatabase import *

def get_schedule(driver):
    """Retrieves the user's schedule with scraping.

    Inputs:
    driver -> Selenium driver object.
    """

    driver = get_page_schedule(driver)
    view_list = driver.find_element(By.XPATH, value = "//div[@title='Mes']")
    driver.execute_script("arguments[0].click();", view_list)
    time.sleep(2)
    cells = driver.find_elements(By.XPATH, "//div[@class='af_calendar_month-time-activity-wrapper']")
    arc = -1

    days = {"0": "Lunes", "1": "Martes", "2": "Miércoles", "3": "Jueves", "4": "Viernes", "5": "Sábado"}
    subject_dic = {"Lunes": [], "Martes": [], "Miércoles": [], "Jueves": [], "Viernes": [], "Sábado": []}

    for cell in cells:
        if cell.get_attribute("arc") == str(arc):
            break

        day = days[cell.get_attribute("arc")]
        subjects = cell.find_elements(by = By.XPATH, value = ".//div[@class='af_calendar_month-time-activity']")

        for subject in subjects:
            driver.execute_script("arguments[0].click();", subject)
            time.sleep(2)
            dialog = driver.find_element(By.XPATH, value="//table[@class='af_dialog_main']")
            name = dialog.find_element(by = By.XPATH, value = ".//td[@class='af_dialog_header-content-center']/div[@class='af_dialog_title']")
            hours = dialog.find_element(by = By.XPATH, value = ".//td[@class='af_dialog_content']/span[3]")
            room = dialog.find_element(by = By.XPATH, value = ".//td[@class='af_dialog_content']/span[4]")
            
            subject_dic.setdefault(day, []).append([name.text, hours.text, room.text])

        arc = 0

    return subject_dic

def add_schedule_user(data):
    """Inserts the data scraped to the database.

    Inputs:
    data -> data to be inserted.
    """

    # Get or create collection
    collection = mongo_db["schedule"]

    # Organize and insert the data
    document = {
        "username": data[0],
        "lunes": data[1],
        "martes": data[2],
        "miercoles": data[3],
        "jueves": data[4],
        "viernes": data[5],
        "sabado": data[6],
    }
    collection.insert_one(document)

def update_schedule_user(data):
    """Updates the user's schedule.

    Inputs:
    data -> data to be updated.
    """

    collection = mongo_db["schedule"]
    username = data[0]
    data = data[1:]

    query = {"username": username}
    update = {"$set": {
        "lunes": data[0],
        "martes": data[1],
        "miercoles": data[2],
        "jueves": data[3],
        "viernes": data[4],
        "sabado": data[5],
    }}
    collection.update_one(query, update)


def schedule(username, data):
    """Adds or updates the user's schedule.

    Inputs:
    username -> string of the student's username.
    data -> data to be added or updated.
    """

    query = {"username": username}
    len_result = mongo_db.schedule.count_documents(query)

    insert_values = [username]
    for _, value in data.items():
        info = ""
        for subject in value:
            info += "\n".join(subject) + "\n---------------\n"

        insert_values.append(info)

    if len_result == 0:
        add_schedule_user(insert_values)
    else:
        update_schedule_user(insert_values)


def generate_schedule_user(username):
    """Returns the student's schedule as a message.

    Inputs:
    username -> string with the student's username.

    Returns:
    A string with the schedule in message format.
    """

    # Query for getting the data
    query = {"username": username}
    # Select which fields to retrieve from the query
    projection = {
        "_id": 0, 
        "lunes": 1,
        "martes": 1,
        "miercoles": 1,
        "jueves": 1,
        "viernes": 1,
        "sabado": 1,
    }
    result = mongo_db.schedule.find_one(query, projection)
    len_result = mongo_db.schedule.count_documents(query)

    days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
    days_fields = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado"]

    if len_result == 0:
        return False
    else:
        message = ""
        for i in range(6):
            message += days[i].upper() + "\n"
            message += result[days_fields[i]] + "\n"
    
    return message
