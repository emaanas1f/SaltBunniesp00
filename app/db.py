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
    c.execute(f"INSERT INTO {table} {tuple(data.keys())} VALUES ({', '.join(placeholder)}) RETURNING *;", tuple(data.values()))
    row = c.fetchall()
    output = dict()
    for col in range(len(row[0])):
        output.update({c.description[col][0]: row[0][col]}) 
    c.close()
    db.commit()
    return output

def general_query(query_string):
    c = db.cursor()
    c.execute(query_string)
    c.close()
    db.commit()
    
#print(select_query("SELECT * FROM profiles WHERE username = ? ", ("U1",))) 
#print(insert_query("profiles", {"username":"U3", "password":"pswd"}))
#print(select_query("SELECT * FROM profiles"))
#print(insert_query("blogs", {"title": "Bg3", "user": "U3"}))
#general_query("INSERT INTO blogs (title, user) VALUES ('Bg3', 'U3')")
#print(select_query("SELECT * FROM blogs"))


