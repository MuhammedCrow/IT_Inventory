from flask import Blueprint, render_template

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("home.html")


@views.route('/computers')
def computers():
    return render_template("computers.html")


@views.route('/monitors')
def monitors():
    return render_template("monitors.html")


@views.route('/printers')
def printers():
    return render_template("printers.html")


@views.route('/network')
def network():
    return render_template("network.html")


@views.route('/cartridges')
def cartridges():
    return render_template("cartridges.html")


@views.route('/addCon', methods=['GET', 'POST'])
def addCon():
    from .db_connect import connect_sql
    conx = connect_sql()
    query = 'INSERT into dbo.consumable (name, categoryId, amount, makeAndModelId) values (?, ?, ?, ?)'
    cursor = conx.cursor()
    cursor.execute(query, 'test', 1, 10, 1)
    conx.comit()
    conx.close()
