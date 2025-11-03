from flask import Flask, render_template, request, flash, redirect, session, url_for
from db_production import select_query, insert_query

app = Flask(__name__)
app.secret_key = "dkjflkaklkjdfsa"

import auth_production
app.register_blueprint(auth_production.bp)

@app.get('/')
def home_get():
    blogs = select_query('SELECT id, title FROM blogs')
    print(blogs)
    return render_template('home.html', blogs=blogs)

@app.get('/blog')
def blog_get():
    title = request.args['title']
    entries = select_query("SELECT id,content FROM entries WHERE blog=? SORT BY date_created", [title])
    return render_template('blog.html', entries=entries)

@app.get('/profile')
def profile_get():
    user = session['username']
    blogs = select_query("SELECT id, title FROM blogs WHERE user=?", [user])
    return render_template('profile.html', blogs=blogs)

@app.post('/profile')
def profile_post():
    title = request.form['title']
    user = session['username']
    if len(select_query("SELECT * FROM blogs WHERE title=?", [title])) != 0:
        flash("Blog with that name already exists!")
        return redirect('/profile')
    new_blog = insert_query("blogs", {"title": title, "user": user})
    return redirect(url_for('blog_get', id=new_blog['id']))

if __name__ == "__main__":
    app.run()
