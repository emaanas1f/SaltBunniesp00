from flask import Flask, render_template, request, flash, redirect, session, url_for
# from db import select_query

app = Flask(__name__)

@app.get('/')
def home_get():
    # blogs = select_query('SELECT id, title FROM blogs')
    blogs = [{"id": 3, "title": "hello"}]
    return render_template('home.html', blogs=blogs)

@app.get('/blog')
def blog_get():
    return

if __name__ == "__main__":
    app.run()
