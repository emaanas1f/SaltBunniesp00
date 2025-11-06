from flask import Flask, render_template, request, flash, redirect, session, url_for
from db import select_query, insert_query, general_query

app = Flask(__name__)
app.secret_key = "dkjflkaklkjdfsa"

import auth_production
app.register_blueprint(auth_production.bp)

@app.get('/')
def home_get():
    blogs = select_query('SELECT id, title FROM blogs')
    return render_template('home.html', blogs=blogs)

@app.get('/profile')
def profile_get():
    user = session['username']
    blogs = select_query("SELECT id, title FROM blogs WHERE author=?", [user])
    return render_template('profile.html', blogs=blogs)

@app.post('/profile')
def profile_post():
    title = request.form['title']
    user = session['username']
    if len(select_query("SELECT * FROM blogs WHERE title=?", [title])) != 0:
        flash("Blog with that name already exists!")
        return redirect('/profile')
    new_blog = insert_query("blogs", {"title": title, "author": user})
    return redirect(url_for('blog_get', id=new_blog['id']))

@app.get('/blog')
def blog_get():
    id = request.args['id']
    entries = select_query("SELECT id,content FROM entries WHERE blog=? ORDER BY date_created", [id])
    blog = select_query("SELECT * FROM blogs WHERE id=?", [id])[0]
    return render_template('blog.html', entries=entries, blog=blog)

@app.get('/create')
def create_get():
    id = request.args['id']
    return render_template('create.html', id=id)

@app.post('/create')
def create_post():
    id = request.args['id']
    content = request.form['content']
    new_entry = insert_query("entries", {"blog": id, "content": content})
    insert_query("edits", {"entry": new_entry['id'], "updated_content": content})
    return redirect(url_for("entry_get", id=id))

@app.get('/entry')
def entry_get():
    id = request.args['id']
    entry = select_query("SELECT * FROM entries WHERE id=?", [id])[0]
    blog = select_query("SELECT * FROM blogs WHERE id=?", [entry['blog']])[0]
    return render_template('entry.html', entry=entry, blog=blog)

@app.get('/edit')
def edit_get():
    id = request.args['id']
    entry = select_query("SELECT id,content FROM entries WHERE id=?", [id])
    return render_template('edit.html', entry=entry)

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
