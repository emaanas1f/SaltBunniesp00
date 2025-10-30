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

@bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('auth.login'))

  # BLAH BLAH BLAH

# @app.route("/login", methods=['GET', 'POST'])
# def disp_loginpage():
#     print("\n\n\n")
#     print("***DIAG: this Flask obj ***")
#     print(app)
#     print("***DIAG: request obj ***")
#     print(request)
#     print("***DIAG: request.args ***")
#     if(request.method == 'GET'):
#         print(request.args)
#         print("***DIAG: request.headers ***")
#         print(request.headers)
#         if 'username' in session:
#             return render_template('home.html', username = session['username'])
#         else:
#             return render_template('login.html')


# @app.route("/auth")
# def authenticate():
#     print("\n\n\n")
#     print("***DIAG: this Flask obj ***")
#     print(app)
#     print("***DIAG: request obj ***")
#     print(request)
#     print(request.args)
#     print("***DIAG: request.args['username']  ***")
#     if(request.method == 'POST'):
#         username = request.form.get('username')
#     else:
#         username = request.args.get('username')
#     if username:
#         session['username'] = username
#         return render_template('home.html', username=username)
#     else:
#         return redirect(url_for('disp_loginpage'))
#     print("***DIAG: request.headers ***")
#     print(request.headers)