import sqlite3

DB_FILE="data.db"

db = sqlite3.connect(DB_FILE)

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
    return out_array

def insert_query(table, data):
    c = db.cursor()
#    insertable_data = []
#    for item in data.values():
#        if isinstance(item, str):
#            insertable_data.append("'" + item + "'")
#        else:
#            insertable_data.append(item)
    # print(insertable_data)
    print(data.values())
    placeholder = ["?"] * len(data)
    c.execute(f"INSERT INTO {table} VALUES ({', '.join(placeholder)});", tuple(data.values()))
    c.close()
    db.commit()

#print(select_query("SELECT * FROM profiles WHERE username = ? ", ("U1",))) 
#insert_query("profiles", {"username":"U3", "password":"pswd"})
#print(select_query("SELECT * FROM profiles"))



