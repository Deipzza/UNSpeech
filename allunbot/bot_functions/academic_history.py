from bs4 import BeautifulSoup
import pandas as pd

from .database.mongodatabase import *
from .utils import *

def get_academic_history(driver = None):
    """Scraps the student's academic history.
    
    Inputs:
    driver -> Selenium driver object

    Returns -> list of rows scraped.
    """

    insert_data = []
    
    # print("Started retrieving data") # Log print

    pag_academic_history = get_page_academic_history(driver)
    page_soup = BeautifulSoup(pag_academic_history, 'html5lib')
    rows = page_soup.find("div", id = "pt1:r1:1:t10::db").find("table").find("tbody").find_all("tr")
    insert_data += select_data_scrap(rows)

    # print("Finalized retrieving data") # Log print

    return insert_data

def academic_history(username, data):
    """Adds or updates the academic history of a user.

    Inputs:
    username -> string of the student's username.
    data -> data to be added or updated.
    """

    query = {"username": username}
    results = mongo_db.academic_history.count_documents(query)
    
    data = pd.DataFrame(data)
    data = data.transpose()
    data = [
        username, "-".join(data[0]), 
        "-".join(data[1]), "-".join(data[2]), 
        "-".join(data[3]), "-".join(data[4]), 
        "-".join(data[5]), "-".join(data[6]),
        "-".join(data[7]), "-".join(data[8])
    ]

    if results < 1:
        add_academic_history_user(mongo_db, data)
    else:
        update_academic_history_user(mongo_db, data)

def add_academic_history_user(db, data):
    """Inserts the data scraped to the database.

    Inputs:
    db -> database connection.
    data -> data to be inserted.
    """

    # print("Started inserting academic history data") # Log print

    # Get or create collection
    collection = db["academic_history"]

    # Organize and insert the data
    document = {
        'username': data[0], 
        'disc_op': data[1], 
        'fund_ob': data[2], 
        'fund_op': data[3],
        'dis_ob': data[4],
        'libre_eleccion': data[5],
        'trabajo_grado': data[6],
        'total': data[7],
        'nivelacion': data[8],
        'total_estudiante': data[9],
    }
    collection.insert_one(document)

    # print("Finalized inserting academic history data") # Log print

def update_academic_history_user(db, data):
    """Updates the academic history for a user.

    Inputs:
    db -> database connection.
    data -> data to be updated.
    """

    # print("Started updating academic history data") # Log print

    collection = db["academic_history"]
    username = data[0]
    data = data[1:]

    query = {"username": username}
    update = {"$set": {
        'disc_op': data[0], 
        'fund_ob': data[1], 
        'fund_op': data[2],
        'dis_ob': data[3],
        'libre_eleccion': data[4],
        'trabajo_grado': data[5],
        'total': data[6],
        'nivelacion': data[7],
        'total_estudiante': data[8],
    }}
    collection.update_one(query, update)

    # print("Finalized updating academic history data") # Log print

def select_data_scrap(rows):
    """Organizes the scraped data to be inserted.

    Inputs:
    rows -> list of table rows retrieved from the web page.

    Returns -> list of formated data
    """

    data = []

    for row in rows:
        cells = row.findAll("td")
        cells = list(map(lambda x: x.text.strip(), cells))
        data.append(cells)
    return data

def generate_academic_history_img(username):
    """Generates an image with the user's academic history.

    Inputs:
    username -> student's username.

    Returns:
    string of the image filename.
    """

    import matplotlib.pyplot as plt
    
    rows = 2
    projection_academic_history = {
        "_id": 0, 
        "disc_op": 1,
        "fund_ob": 1,
        "fund_op": 1,
        "dis_ob": 1,
        "libre_eleccion": 1,
        "trabajo_grado": 1,
        "total": 1,
        "nivelacion": 1,
        "total_estudiante": 1,
    }
    projection_metrics = {
        "_id": 0, 
        "papa": 1,
        "promedio": 1,
        "avance": 1,
    }

    query = {"username": username}
    academic_history = mongo_db.academic_history.find_one(query, 
                                                    projection_academic_history)
    len_academic_history = mongo_db.academic_history.count_documents(query)
    metrics = mongo_db.metrics.find_one(query, projection_metrics)
    len_metrics = mongo_db.metrics.count_documents(query)

    if len_academic_history == 0 or len_metrics == 0:
        rows -= 1
    elif len_academic_history == 0 and len_metrics == 0:
        return "Lo sentimos, no hemos podido encontrar tu historia academica, comunicate con el área de soporte."
    
    fig, (table1, table2) = plt.subplots(2, 1, sharey = True)

    if len_academic_history != 0:
        academic_column_headers = ('Exigidos', 'Aprobados', 'Pendientes', 'Inscritos', 'Cursados')
        academic_history_data = [value.split("-") for _, value in academic_history.items()]
        metrics_data = [[value for _, value in metrics.items()]]
        
        # Pop the headers from the data array
        row_headers = [x.pop(0) for x in academic_history_data]
        table2.table(
            cellText = academic_history_data,
            rowLabels = row_headers,
            colLabels = academic_column_headers,
            loc = 'center'
        )

    if len_metrics != 0:
        metrics_column_headers = ['P.A.P.A', 'Promedio', "Avance"]
        table1.table(
            cellText = metrics_data,
            colLabels = metrics_column_headers,
            loc = 'center'
        )
    
    # Hide axes
    fig.patch.set_visible(False)
    table1.axis('off')
    table1.axis('tight')
    table2.axis('off')
    table2.axis('tight')
    fig.tight_layout()

    temp_folder = create_temp()
    filename = os.path.join(temp_folder, f'{username}-academic-history.png')
    plt.savefig(filename, bbox_inches = 'tight')

    return filename

def create_temp():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    temp = os.path.join(BASE_DIR, os.path.join("bot_functions", "temp"))

    if not os.path.exists(temp):
        os.mkdir(temp)

    return temp
