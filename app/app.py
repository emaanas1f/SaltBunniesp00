from flask import Flask, render_template, request, flash, redirect, session, url_for
from db import select_query, insert_query, general_query

app = Flask(__name__)
app.secret_key = "dkjflkaklkjdfsa"

import auth
app.register_blueprint(auth.bp)

# displays all blogs
@app.get('/')
def home_get():
    blogs = select_query('SELECT id, title FROM blogs')
    return render_template('home.html', blogs=blogs)

# display created blogs
@app.get('/profile')
def profile_get():
    user = session['username']
    blogs = select_query("SELECT id, title FROM blogs WHERE author=?", [user])
    return render_template('profile.html', blogs=blogs)

# create blog
@app.post('/profile')
def profile_post():
    title = request.form['title']
    user = session['username']
    if len(select_query("SELECT * FROM blogs WHERE title=?", [title])) != 0:
        flash("Blog with that name already exists!")
        return redirect('/profile')
    new_blog = insert_query("blogs", {"title": title, "author": user})
    return redirect(url_for('blog_get', id=new_blog['id']))

# display selected blog
@app.get('/blog')
def blog_get():
    id = request.args['id']
    entries = select_query("SELECT id,content FROM entries WHERE blog=? ORDER BY date_created", [id])
    general_query("UPDATE blogs SET views=views+1 WHERE id=?", [id])
    return render_template('blog.html', entries=entries)

#use blog_post for follow

def translate_to(dictionary):
    output = ""
    # p-lorem ipsum|||
    for key in dictionary:
        output += key.split('-', 1)[1]
        output += "-"
        output += dictionary[key].replace('|', "\|")
        output += "|||"
    output = output[:-3]
    return output

def translate_from(string):
    output = {}
    # {"p": "lorem ipsum"}
    partial = string.split("|||")
    for field in partial:
        field = field.replace("\|", "|")
        field = field.split("-", 1)
        output[field[0]] = field[1]
    return output

@app.get('/create')
def create_get():
    id = request.args['id']
    return render_template('create.html', id=id)

@app.post('/create')
def create_post():
    id = request.args['id']
    content = translate_to(request.form['content'])
    new_entry = insert_query("entries", {"blog": id, "content": content})
    insert_query("edits", {"entry": new_entry['id'], "updated_content": content})
    return redirect(url_for("entry_get", id=id))

# display specific entry
@app.get('/entry')
def entry_get():
    id = request.args['id']
    entry = select_query("SELECT * FROM entries WHERE id=?", [id])[0]
    entry[]
    blog = select_query("SELECT * FROM blogs WHERE id=?", [entry['blog']])[0]
    next = select_query("SELECT * FROM entries WHERE blog=? AND id>? LIMIT 1", [entry['blog'], id])
    prev = select_query("SELECT * FROM entries WHERE blog=? AND id<? LIMIT 1", [entry['blog'], id])
    return render_template('entry.html', entry=entry, blog=blog, next=next, prev=prev)

# get content to edit entry
@app.get('/edit')
def edit_get():
    id = request.args['id']
    entry = select_query("SELECT id,content FROM entries WHERE id=?", [id])
    return render_template('edit.html', entry=entry)

# update entry with new content
@app.post('/edit')
def edit_post():
    id = request.args['id']
    content = request.form['content']
    user = session['username']
    new_edit = insert_query("edits", {"entry": id, "user": user, "updated_content": content})
    general_query("UPDATE entries SET content=?,recent_edit=? WHERE id=?", [content, new_edit['timestamp'], id])
    return redirect(url_for("entry_get", id=id))

if __name__ == "__main__":
    app.run()
