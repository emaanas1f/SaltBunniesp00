from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db_production import select_query, insert_query

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.get('/signup')
def signup_get():
    return render_template('auth/signup.html')

@bp.post('/signup')
def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')
    if len(select_query("SELECT * FROM profiles WHERE username=?", [username])) != 0:
        flash('Username already exists.', 'error')
        return redirect(url_for('auth.signup_get'))
    insert_query("profiles", {"username": username, "password": password})
    flash('Sign up successful! Please log in.', 'success')
    return redirect(url_for('auth.login_get'))

@bp.get('/login')
def login_get():
    return render_template('auth/login.html')

@bp.post('/login')
def login_post():
    session['username'] = request.form.get('username')
    return redirect(url_for('home_get'))

@bp.get('/logout')
def logout_get():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login_get'))