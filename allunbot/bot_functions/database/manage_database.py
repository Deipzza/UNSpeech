import sqlite3


db = 'allunbot.db'
def create_tables(db):
    with open('create_table.sql', 'r') as sql_file:
        sql_script = sql_file.read()

    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.executescript(sql_script)
    con.commit()
    con.close()

def create_table(db, table, query):
    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute(f"DROP TABLE IF EXISTS {table}")
    cur.execute(query)
    con.commit()
    con.close()

def insert_values_by_query(insert_data, db, sql):
    con = sqlite3.connect(db)
    cur = con.cursor() 
    cur.executemany(sql, insert_data)
    con.commit()
    con.close()


def select_data_query(sql, db, params = []):
    con = sqlite3.connect(db)
    cur = con.cursor()

    consulta = []
    for element in cur.execute(sql, params):
        consulta.append(element)

    con.close()
    return consulta

def update_data_query(sql, db, params = []):
    """Updates the DB with the specified SQL"""

    con = sqlite3.connect(db)
    cur = con.cursor()

    cur.execute(sql, params)
    con.commit()
    con.close()

def select_data_all(table, db):
    con = sqlite3.connect(db)
    cur = con.cursor()

    consulta = []
    for element in cur.execute("SELECT * FROM ?",(table,)):
        consulta.append(element)

    con.close()
    return consulta