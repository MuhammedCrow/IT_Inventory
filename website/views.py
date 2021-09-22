from flask import Blueprint, render_template, request
from werkzeug.utils import redirect

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("home.html")


@views.route('/computers')
def computers():
    from .db_connect import connect_sql
    conx = connect_sql()
    query = 'Select dbo.make.name, dbo.model.name from dbo.model inner join dbo.make on dbo.make.id = dbo.model.makeId'
    cursor = conx.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return render_template("computers.html", data=data)


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
    category1 = request.form.get('category')
    condition1 = request.form.get('condition')
    condition = 0
    category = 0
    print(condition1)
    if condition1 == 'New':
        condition = 1
    elif condition1 == 'Used':
        condition = 2
    else:
        condition = 3

    if category1 == 'Desktop':
        category = 4
    else:
        category = 3
    print(condition)
    print(category)
    from .db_connect import connect_sql
    conx = connect_sql()
    query = 'insert into hardware(serialNumber, categoryId, makeAndModel, condition) values (?,?,?,?)'
    cursor = conx.cursor()
    cursor.execute(query, snumber, category, 2, condition)
    conx.commit()
    conx.close()
    return redirect('/computers')


@views.route('/issueComputer', methods=['GET', 'POST'])
def issueComputer():
    snumber = request.form.get('snumber')
    useremail = request.form.get('user')
    date = request.form.get('date')
    from .db_connect import connect_sql
    conx = connect_sql()
    getuserId = 'select id from dbo.clients where email = ?'
    query = 'update dbo.hardware set userId = ? , receiveDate = ? where dbo.hardware.serialNumber = ?'
    cursor = conx.cursor()
    cursor.execute(getuserId, useremail)
    data = cursor.fetchall()
    userId = data[0][0]
    cursor.execute(query, userId, date, snumber)
    conx.commit()
    conx.close()
    return redirect('/computers')
