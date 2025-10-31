from flask import Flask, render_template, request, flash, redirect, session, url_for
from db import select_query, insert_query

app = Flask(__name__)

import auth
app.register_blueprint(auth.bp)

@app.get('/')
def home_get():
    blogs = select_query('SELECT id, title FROM blogs')
    return render_template('home.html', blogs=blogs)

@app.get('/profile')
def profile_get():
    user = session['username']
    blogs = select_query("SELECT id, title FROM blogs WHERE user='?'", [user])
    return render_template('profile.html', blogs=blogs)

@app.post('/profile')
def profile_post():
    title = request.form['title']
    content = request.form['content']
    user = session['username']
    if len(select_query("SELECT * FROM blogs WHERE title='?'", [title])) != 0:
        flash("Blog with that name already exists!")
        return redirect('/profile')
    new_blog = insert_query("blogs", {"title": title, "user": user, "content": content})
    return redirect(url_for('blog_get', id=new_blog['id']))

@app.get('/blog')
def blog_get():
    title = request.args['title']
    entries = select_query("SELECT id,content FROM entries WHERE blog='?' SORT BY date_created", [title])
    return render_template('blog.html', entries=entries)

@app.post('/blog')
def blog_post():
    id = request.args['id']
    return render_template('create.html', id=id)

@app.get('/entry')
def entry_get():
    id = request.args['id']
    entry = select_query("SELECT content,date_created FROM entries WHERE id=?", [id])
    return render_template('post.html', entry=entry)

@app.get('/create')
def create_get():
    id = request.args['id']
    return render_template('create.html', id=id)

@app.post('/create')
def create_post():
    id = request.args['id']
    content = request.form['content']
    user = session['username']
    new_entry = insert_query("entries", {"blog": id, "content": content, "user": user})
    new_edit = insert_query("edits", {"entry": new_entry['id'], "updated_content": content})
    return redirect(url_for("entry_get", id=id))

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
    general_query("UPDATE entries SET content='?',recent_edit='?' WHERE id=?", [content, new_edit['timestamp'], id])
    return redirect(url_for("entry_get", id=id))
