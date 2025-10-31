from flask import Flask, render_template, request, flash, redirect, session, url_for
from db_production import select_query

app = Flask(__name__)

import auth_production
app.register_blueprint(auth_production.bp)

@app.get('/')
def home_get():
    blogs = select_query('SELECT id, title FROM blogs')
    return render_template('home.html', blogs=blogs)

@app.get('/blog')
def blog_get():
    return request.args['title']

if __name__ == "__main__":
    app.run()
