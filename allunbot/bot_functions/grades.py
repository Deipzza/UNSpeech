import regex

from .login import *
from .functions_utils import *

def get_grades(driver):
    """Extracts the grades from the page.
    
    Inputs:
    driver -> Selenium driver.
    
    Returns:
    dictionary with the grade from each subject.
    """

    driver = get_page_grades(driver)
    
    tabla = driver.find_element(By.CSS_SELECTOR, "span.nota-listado")
    total_rows = len(tabla.find_elements(
        By.XPATH, ".//span[@class='row af_panelGroupLayout']"
    ))

    subject_dic = {}

    for i_row in range(total_rows):

        # Defaults values
        grades_dic = {"data_table": [], "grades": []}
        posible_grade = 0

        # My subjects in this semester
        tabla = driver.find_element(By.CSS_SELECTOR, "span.nota-listado")
        row = tabla.find_elements(
            By.XPATH, ".//span[@class='row af_panelGroupLayout']"
        )[i_row]

        try:  # If there are blank rows.
            name_subject = row.find_element(By.CSS_SELECTOR,
                                            value = ".nota-nombre-asignatura")
            grade = row.find_element(By.CSS_SELECTOR,
                                     value = "span.nota-calificacion").text
        except:
            continue
        
        # Extract the principal information subject
        subject, serial = name_subject.text.split("(")
        subject, serial = subject[:-1], serial[:-1]
        
        # Go to the grades page
        name_subject.click()
        time.sleep(3)
        
        # Find more information about subject (credit and tipology)
        more_info = driver.find_elements(
            By.CSS_SELECTOR,
            "span.nota-detalle-datos-academicos > span.salto span"
        )
        tipology = more_info[0].text[11:]
        credito = more_info[1].text[-1]

        # Obtains grades
        rows_grades = driver.find_elements(By.CSS_SELECTOR,
                                           "span.bloque-row.datos-parcial")
        for row_grade in rows_grades:

            por_grade = row_grade.find_element(
                by = By.CSS_SELECTOR, value ="span.datos-parcial-porcentaje"
            ).text
            por_grade = regex.sub("(%)|(nota final)|\s", "", por_grade)
            if por_grade.isnumeric(): por_grade = int(por_grade)
            else: continue
            
            name_grade = verify_exist("span.datos-parcial-descripcion",
                                      row_grade)
            name_grade = "Nota total" if not name_grade else name_grade

            nota = verify_exist("span.datos-parcial-calificacion", row_grade)
            nota = 0 if not nota else nota
            nota = float(nota)

            posible_grade += nota * por_grade / 100

            grades_dic["grades"].append([name_grade, por_grade, nota])


        if "SIN DEFINITIVA" in grade:
            grades_dic["data_table"] = [subject, credito, tipology,
                                        round(posible_grade,1)]
        else:
            grades_dic["data_table"] = [subject, credito, tipology,
                                        regex.sub(r"(APROBADA)|(REPROBADA)", "",
                                        grade)]

        subject_dic[serial] = grades_dic
        driver.find_element(By.CSS_SELECTOR,
                            value = ".af_region .af_button.p_AFTextOnly"
        ).click()
        time.sleep(3)
        
    return subject_dic


def add_grades_user(data, username):
    """Inserts the data scraped to the database.

    Inputs:
    db -> database connection.
    data -> data to be inserted.
    """

    # Get or create collection
    collection = mongo_db["grades"]

    # Organize and insert the data
    document = {
        'username': username, 
        'data': data
    }
    collection.insert_one(document)


def update_grades_user(data, username):
    """Updates the academic history for a user.

    Inputs:
    db -> database connection.
    data -> data to be updated.
    """

    collection = mongo_db["grades"]

    query = {"username": username}
    update = {"$set": {
        'data': data
    }}
    collection.update_one(query, update)


def grades(username, data):
    """Adds or updates the academic history of a user.

    Inputs:
    username -> string of the student's username.
    data -> data to be added or updated.
    """
    
    query = {"username": username}
    results = mongo_db.grades.count_documents(query)

    if results < 1:
        add_grades_user(data, username)
    else:
        update_grades_user(data, username)


def verify_exist(value, row_grade):
    """Verify if a field of grades exists within the subject.
    
    Inputs:
    value -> string with the CSS selector for the search.
    row_grade -> subject to search.

    Returns:
    the element if it's found, False otherwise.
    """

    try:
        grade_element = row_grade.find_element(by = By.CSS_SELECTOR,
                                               value = value).text
        return grade_element
    
    except:
        return False
