import sqlite3

DB_FILE="data.db"

db = sqlite3.connect(DB_FILE)
c = db.cursor()

def select_query(query_string, parameters):
    outstring = query_string
    c.execute(query_string, (parameters)) #FINISH
    return c.fetchall()
