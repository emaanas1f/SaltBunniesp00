import sqlite3

DB_FILE="data.db"

db = sqlite3.connect(DB_FILE)
c = db.cursor()


c.executescript("""
    DROP TABLE IF EXISTS profiles;
    CREATE TABLE profiles (username TEXT PRIMARY KEY, password TEXT);
    DROP TABLE IF EXISTS blogs;
    CREATE TABLE blogs (id INTEGER PRIMARY KEY, title TEXT, user TEXT, date_created DATETIME, FOREIGN KEY (user) REFERENCES profile(username));
    DROP TABLE IF EXISTS entries;
    CREATE TABLE entries (blog INTEGER, id INTEGER PRIMARY KEY, date_created DATETIME, content TEXT, recent_edit DATETIME, FOREIGN KEY (blog) REFERENCES blogs(id));
    DROP TABLE IF EXISTS edits;
    CREATE TABLE edits (entry_id INTEGER, user TEXT, timestamp DATETIME, updated_content TEXT, FOREIGN KEY (entry_id) REFERENCES entries(id), FOREIGN KEY (user) REFERENCES profile(username));
    """)

#c.execute("INSERT INTO profiles VALUES ('U1', 'pwrd1');")
#c.execute("INSERT INTO profiles VALUES ('U2', 'pwrd2');")
db.commit()
db.close()
