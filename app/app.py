from flask import Flask, render_template, request, flash, redirect
from db import select_query, insert_query

app = Flask(__name__)

import auth
app.register_blueprint(auth.bp)

@app.route('/', methods=['GET'])
def home():
    blogs = select_query('SELECT blog_name FROM blogs')
    return render_template('home.html', blogs)

@app.route('/profile', methods=['GET'])
def get_profile():
    username = request.args['username']
    blogs = select_query("SELECT blog_name FROM blogs WHERE user='?'", [username])
    return render_template('profile.html', blogs)

@app.route('/profile', methods=['POST'])
def post_profile():
    blog_name = request.form['name']
    content = request.form['content']
    if len(select_query('SELECT * FROM blogs WHERE blog_name=?', [blog_name])) != 0:
        flash("Blog with that name already exists!")
        return redirect('/profile')
    inset_query("INSERT into REQUESTS () ## COMPELTE

@app.route('/blog', methods=['GET'])
def blog():
    blog_name = request.args['name']
    entries = select_query("SELECT id,content FROM entries WHERE blog='?' SORT BY date_created", [blog_name])
    return render_template('blog.html', entries)

@app.route('/post', methods=['GET'])
def post():
    post_id = request.args[]
    return render_template('post.html')


@app.route('/edit', methods=['POST'])
def edit():
    if (request.args['type'] == 'create_blog'): ## COMPLETE