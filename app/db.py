import sqlite3

DB_FILE="data.db"

db = sqlite3.connect(DB_FILE)
c = db.cursor()

def select_query(query_string, parameters=()):
    c.execute(query_string, parameters)
    out_array = []
    column_names = c.description
    for row in c.fetchall():
        item_dict = dict()
        for col in range(len(row)):
             item_dict.update({column_names[col][0]: row[col]})
        out_array.append(item_dict)
    return out_array

print(select_query("SELECT * FROM profiles WHERE username = ? ", ("U1",))) 

# general query function
# insert-query function
db.commit()
db.close()
