from flask import Flask, render_template, request, flash, redirect, session, url_for
# from db import select_query

app = Flask(__name__)

@app.get('/')
def home_get():
    return render_template('home.html')

if __name__ == "__main__":
    app.run()