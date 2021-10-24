from flask import Blueprint, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
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
    return "<p>logout</p>"
