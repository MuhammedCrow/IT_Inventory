from flask import Blueprint, render_template, request, session, flash
from flask.helpers import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
# from flask_login import login_user, login_required, logout_user, current_user
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.permanent = True
        userName = request.form.get('username')
        password = request.form.get('password')
        from .db_connect import connect_sql
        conx = connect_sql()
        query = 'SELECT username, password from dbo.admin where username = ?'
        cursor = conx.cursor()
        cursor.execute(query, userName)
        row1 = cursor.fetchone()
        if not row1:
            flash('User Not Found', category='error')
            return render_template("login.html")
        else:
            if check_password_hash(row1.password, password):
                session["user"] = row1.username
                flash('Log in Successful', category='success')
                return render_template("home.html", user=row1.username)
            else:
                flash('Wrong Password', category='error')
                return render_template("login.html")

    else:
        return render_template("login.html")


@auth.route('/addAdmin', methods=['GET', 'POST'])
def addAdmin():
    userName = request.form.get('name')
    password = request.form.get('pass')
    hashedPass = generate_password_hash(password, method='sha256')
    from .db_connect import connect_sql
    conx = connect_sql()
    query = 'insert into dbo.admin(username,password) values (?,?)'
    cursor = conx.cursor()
    cursor.execute(query, userName, hashedPass)
    conx.commit()
    conx.close()
    return render_template("adminConsole.html")


@auth.route('/logout')
def logout():
    session.pop("user", None)
    flash('Logout Successful', category='success')
    return redirect(url_for("auth.login"))
