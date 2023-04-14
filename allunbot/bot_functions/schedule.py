import os
import time

from .utils import *
from .login import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
temp = os.path.join(BASE_DIR, 'allunbot/bot_functions/temp')
db = os.path.join(BASE_DIR, 'allunbot.db')

def get_schedule(driver):
    driver = get_page_schedule(driver)
    view_list = driver.find_element(By.XPATH, value="//div[@title='Mes']")
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


def create_table_schedule():
    query = """
        CREATE TABLE schedule(
            username TEXT PRIMARY KEY, 
            lunes TEXT,
            martes TEXT,
            miercoles TEXT,
            jueves TEXT,
            viernes TEXT,
            sabado TEXT
        );
        """
    create_table(db, "schedule", query)


def add_schedule_user(data):
    sql = """
        INSERT INTO
            schedule
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
    insert_values_by_query([data], db, sql)


def update_schedule_user(data):
    sql = """
        UPDATE schedule
            SET
            lunes = ?,
            martes = ?,
            miercoles = ?,
            jueves = ?,
            viernes = ?,
            sabado = ?
            WHERE
            username = ?
        """
    
    username = data[0]
    data = data[1:]
    data.append(username)
    update_data_query(sql, db, data)


def schedule(username, data):
    """
    """

    sql = "SELECT * FROM schedule WHERE username = ?;"
    result = select_data_query(sql, db, [username])

    insert_values = [username]
    for _, value in data.items():
        info = ""
        for subject in value:
            info += "\n".join(subject) + "\n---------------\n"

        insert_values.append(info)

    if len(result) == 0:
        add_schedule_user(insert_values)
    else:
        update_schedule_user(insert_values)


def generate_schedule_user(username):
    sql = "SELECT * FROM schedule WHERE username = ?"
    result = select_data_query(sql, db, [username])[0][1:]
    days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]

    if len(result) == 0:
        return False
    else:
        message = ""
        for i in range(len(result)):
            message += days[i].upper() + "\n"
            message += result[i] + "\n"
    
    return message

# Not implemented yet
def generate_schedule_img(username):
    import matplotlib.pyplot as plt

    sql = "SELECT * FROM schedule WHERE username = ?"
    result = select_data_query(sql, db, [username])

    if len(result) == 0:
        return False
    
    column_headers = ('Exigidos', 'Aprobados', 'Pendientes', 'Inscritos', 'cursados')
    data = [item.split("-") for item in result[0][1:]]
    fig, ax = plt.subplots()

    # Pop the headers from the data array
    row_headers = [x.pop(0) for x in data]
    ax.table(cellText = data,
            rowLabels = row_headers,
            colLabels = column_headers,
            loc = 'center')
    
    # Hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    fig.tight_layout()

    filename= os.path.join(temp, f'{username}-academic-history.png')
    plt.savefig(filename, bbox_inches = 'tight', dpi = 150)

    return filename


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
