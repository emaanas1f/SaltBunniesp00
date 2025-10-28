from flask import Blueprint

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET'])
def get_login():
  return
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