from flask import Blueprint, render_template, request
from werkzeug.utils import redirect

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
    from .db_connect import connect_sql
    conx = connect_sql()
    query = 'select name from consumable where makeAndModle = 1'
    cursor = conx.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return render_template("cartridges.html", data=data)


@views.route('/addCon', methods=['GET', 'POST'])
def addCon():
    amount = int(request.form.get('amount'))
    model = request.form.get('model')
    from .db_connect import connect_sql
    conx = connect_sql()
    query = 'update dbo.consumable SET amount += ? where dbo.consumable.name = ?'
    cursor = conx.cursor()
    cursor.execute(query, amount, model)
    conx.commit()
    conx.close()
    return redirect('/cartridges')


@views.route('/issueCon', methods=['GET', 'POST'])
def issueCon():
    amount = int(request.form.get('amount'))
    model = request.form.get('model')
    date = request.form.get('date')
    from .db_connect import connect_sql
    conx = connect_sql()
    query = 'update dbo.consumable SET amount -= ? where dbo.consumable.name = ?'
    cursor = conx.cursor()
    cursor.execute(query, amount, model)
    conx.commit()
    conx.close()
    return redirect('/cartridges')


@views.route('/addComputer', methods=['GET', 'POST'])
def addComputer():
    snumber = request.form.get('snumber')
    model = request.form.get('model')
    condition = request.form.get('condition')
    from .db_connect import connect_sql
    conx = connect_sql()
    query = 'insert into hardware(serialNumber, categoryId, makeAndModel,'
    cursor = conx.cursor()
    cursor.execute(query, amount, model)
    conx.commit()
    conx.close()
    return redirect('/cartridges')
