from flask import Flask, render_template, request, flash, redirect, session, url_for
from db_production import select_query, insert_query

app = Flask(__name__)
app.secret_key = "dkjflkaklkjdfsa"

import auth_production
app.register_blueprint(auth_production.bp)

@app.get('/')
def home_get():
    blogs = select_query('SELECT id, title FROM blogs')
    return render_template('home.html', blogs=blogs)

@app.get('/blog')
def blog_get():
    return request.args['title']

@app.get('/profile')
def profile_get():
    user = session['username']
    blogs = select_query("SELECT id, title FROM blogs WHERE user=?", [user])
    return render_template('profile.html', blogs=blogs)

@app.post('/profile')
def profile_post():
    title = request.form['title']
    content = request.form['content']
    user = session['username']
    if len(select_query("SELECT * FROM blogs WHERE title=?", [title])) != 0:
        flash("Blog with that name already exists!")
        return redirect('/profile')
    new_blog = insert_query("blogs", {"title": title, "user": user, "content": content})
    return redirect(url_for('blog_get', id=new_blog['id']))

if __name__ == "__main__":
    app.run()
