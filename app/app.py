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
    insert_query("blogs", {"title": title, "user": user, "content": content})
    id = select_query("SELECT id FROM blogs WHERE title='?'", [title])
    return redirect(url_for('blog_get', id=id))

@app.get('/blog')
def blog_get():
    title = request.args['title']
    entries = select_query("SELECT id,content FROM entries WHERE blog='?' SORT BY date_created", [title])
    return render_template('blog.html', entries=entries)

@app.get('/entry')
def entry_get():
    post_id = request.args[]
    return render_template('post.html')

@app.post('/edit')
def edit_post():
    if (request.args['type'] == 'create_blog'): ## COMPLETE