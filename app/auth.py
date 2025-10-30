from flask import Blueprint, render_template, request, redirect, url_for, session

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            session['username'] = username
            return redirect(url_for('auth.home'))
        else:
            return render_template('login.html', error='Please enter a username')

    return render_template('login.html')

@bp.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    return render_template('home.html', username=session['username'])

#logout 
@bp.route('/logout')
   def logout():
   session.pop('username', None)
    return redirect(url_for('auth.login'))


