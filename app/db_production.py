import sqlite3

DB_FILE="data.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False)

def select_query(query_string, parameters=()):
    c = db.cursor()
    c.execute(query_string, parameters)
    out_array = []
    column_names = c.description
    for row in c.fetchall():
        item_dict = dict()
        for col in range(len(row)):
             item_dict.update({column_names[col][0]: row[col]})
        out_array.append(item_dict)
    c.close()
    db.commit()
    return out_array

def insert_query(table, data):
    c = db.cursor()
    placeholder = ["?"] * len(data)
    c.execute(f"INSERT INTO {table} VALUES ({', '.join(placeholder)}) RETURNING rowid;", tuple(data.values()))
    row = c.fetchall()[0][0]
    c.close()
    db.commit()
    output = dict(row = row)
    return output


