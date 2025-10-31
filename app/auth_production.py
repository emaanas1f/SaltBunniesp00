from flask import Blueprint, render_template, request, redirect, url_for, session

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            session['username'] = username
            return redirect(url_for('home_get'))
        else:
            return render_template('auth/login.html', error='Please enter a username')
    return render_template('auth/login.html')