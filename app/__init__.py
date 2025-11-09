from flask import Flask, render_template, request, flash, redirect, session, url_for
from db import select_query, insert_query, general_query
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "dkjflkaklkjdfsa"

import auth
app.register_blueprint(auth.bp)

@app.before_request
def check_authentification():
    if 'username' not in session.keys() and request.blueprint != 'auth' and request.endpoint != 'static':
        flash("Please log in to view our website")
        return redirect(url_for("auth.login_get"))

# displays all blogs
@app.get('/')
def home_get():
    blogs = select_query('SELECT id, title, author FROM blogs')
    return render_template('home.html', blogs=blogs)

# display created blogs
@app.get('/profile')
def profile_get():
    user = session['username']
    user_blogs = select_query("SELECT id, title FROM blogs WHERE author=?", [user])
    followed_blogs = select_query("SELECT blogs.id, blogs.title FROM follows JOIN blogs ON follows.blog = blogs.id WHERE follows.user=?", [user])
    return render_template('profile.html', user_blogs=user_blogs, followed_blogs=followed_blogs, user = user)

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
    followed = select_query("SELECT * FROM follows WHERE user=? AND blog=?", [session["username"], id])
    entries = select_query("SELECT id,content FROM entries WHERE blog=? ORDER BY date_created", [id])
    general_query("UPDATE blogs SET views=views+1 WHERE id=?", [id])
    blog = select_query("SELECT * FROM blogs WHERE id=?", [id])[0]
    return render_template('blog.html', entries=entries, blog=blog, followed=followed)

#update follow counter and table on follow
@app.get('/follow')
def follow_get():
    id = request.args['id']
    user = session["username"]
    insert_query("follows", {"user": user, "blog": id})
    general_query("UPDATE blogs SET follows=follows+1 WHERE id=?", [id])
    return redirect(url_for('blog_get', id=id))

def translate_to(dictionary):
    output = ""
    # p-lorem ipsum|||
    for key in dictionary:
        dictionary[key].replace('|', "\|")
        output += f"{key}-{dictionary[key]}|||"
    output = output[:-3]
    return output

def translate_from(string):
    output = []
    # [("p", "lorem ipsum")]
    partial = string.split("|||")
    for field in partial:
        field = field.replace("\|", "|")
        field = field.split("-", 1)
        field[1] = field[1].replace("\n", "<br>")
        output.append({"type": field[0], "content": field[1]})
    return output

@app.get('/create')
def create_get():
    id = request.args['id']
    return render_template('create.html', id=id)

# create entry
@app.post('/create')
def create_post():
    id = request.args['id']
    content = translate_to(request.form)
    new_entry = insert_query("entries", {"blog": id, "content": content})
    insert_query("edits", {"entry": new_entry['id'], "updated_content": content})
    return redirect(url_for("entry_get", id=new_entry["id"]))

# display specific entry
@app.get('/entry')
def entry_get():
    id = request.args['id']
    entry = select_query("SELECT * FROM entries WHERE id=?", [id])[0]
    entry['content'] = translate_from(entry['content'])
    entry['date_created'] = datetime.strptime(entry['date_created'], "%Y-%m-%d %H:%M:%S") - timedelta(hours=5)
    blog = select_query("SELECT * FROM blogs WHERE id=?", [entry['blog']])[0]
    next = select_query("SELECT * FROM entries WHERE blog=? AND id>? LIMIT 1", [entry['blog'], id])
    prev = select_query("SELECT * FROM entries WHERE blog=? AND id<?", [entry['blog'], id])
    return render_template('entry.html', entry=entry, blog=blog, next=next, prev=prev)

# get content to edit entry
@app.get('/edit')
def edit_get():
    id = request.args['id']
    entry = select_query("SELECT id,content FROM entries WHERE id=?", [id])[0]
    entry['content'] = translate_from(entry['content'])
    return render_template('edit.html', entry=entry)

# update entry with new content
@app.post('/edit')
def edit_post():
    id = request.args['id']
    content = translate_to(request.form)
    new_edit = insert_query("edits", {"entry": id, "updated_content": content})
    general_query("UPDATE entries SET content=?,recent_edit=? WHERE id=?", [content, new_edit['timestamp'], id])
    return redirect(url_for("entry_get", id=id))

if __name__ == "__main__":
    app.run()