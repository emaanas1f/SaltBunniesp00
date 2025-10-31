from flask import Blueprint, render_template, request, redirect, url_for, session, flash

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.get('/signup')
def signup_get():
    return render_template('auth/signup.html')

@bp.post('/signup')
def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')
    if len(select_query("SELECT * FROM profiles WHERE username='?'", [username])) != 0:
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
    username = request.form.get('username')
    password = request.form.get('password')
    if len(select_query("SELECT * FROM profiles WHERE username='?'", [username])) !=0
        flash(f'Welcome back, {username}!', 'success')
        return redirect(url_for('auth.home_get'))
    else:
        flash('Invalid username or password.', 'error')
        return redirect(url_for('auth.login_get'))

@bp.get('/home')
def home_get():
    if 'username' not in session:
        flash('Please log in to continue.', 'error')
        return redirect(url_for('auth.login'))
    return render_template('home.html', username=session['username'])

@bp.get('/logout')
def logout_get():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
