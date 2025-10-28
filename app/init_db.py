import sqlite3

DB_FILE="data.db"

db = sqlite3.connect(DB_FILE)
c = db.cursor()


c.execute("DROP TABLE IF EXISTS profile") # check for already existing entries table
c.execute("CREATE TABLE profiles (username TEXT PRIMARY KEY, password TEXT);")

c.execute("DROP TABLE IF EXISTS blogs")
c.execute("CREATE TABLE blogs (blog_id INTEGER PRIMARY KEY, blog_name TEXT, user TEXT, date_created DATETIME, FOREIGN KEY (user) REFERENCES profile(username));")

c.execute("DROP TABLE IF EXISTS entries") 
c.execute("CREATE TABLE entries (blog INTEGER, id INTEGER PRIMARY KEY, date_created DATETIME, content TEXT, recent_edit DATETIME, FOREIGN KEY (blog) REFERENCES blogs(blog_id));")

c.execute("DROP TABLE IF EXISTS edits")
c.execute("CREATE TABLE edits (entry_id INTEGER, user TEXT, timestamp DATETIME, updated_content TEXT, FOREIGN KEY (entry_id) REFERENCES entries(id), FOREIGN KEY (user) REFERENCES profile(username));")


db.commit()
db.close()
