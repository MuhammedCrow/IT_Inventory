from flask import Blueprint, render_template, request
from werkzeug.utils import redirect

views = Blueprint('views', __name__)
results = 0
hardware = []
consumables = []
Gdate = 0


def fetchMakeAndModel():
    from .db_connect import connect_sql
    conx = connect_sql()
    query = 'Select dbo.make.name, dbo.model.name from dbo.model inner join dbo.make on dbo.make.id = dbo.model.makeId'
    cursor = conx.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    return data


def addToCart(snumber):
    from .db_connect import connect_sql
    conx = connect_sql()
    cursor = conx.cursor()
    fetchQuery = 'SELECT dbo.hardware.serialNumber, dbo.hardware.receiveDate, dbo.make.name, dbo.model.name from dbo.hardware INNER JOIN dbo.model on dbo.hardware.makeAndModel = dbo.model.id INNER JOIN dbo.make on dbo.model.makeId = dbo.make.id INNER JOIN dbo.consumableCat on dbo.hardware.categoryId = dbo.consumableCat.id where dbo.hardware.serialNumber = ? order by dbo.hardware.receiveDate asc;'
    cursor.execute(fetchQuery, snumber)
    hd = cursor.fetchall()
    for row in hd:
        global hardware
        hardware.append(row)
    conx.close()


@views.route('/')
def home():
    return render_template("home.html")


@views.route('/clients')
def clients():
    return render_template("clients.html")


@views.route('/computers')
def computers():
    data = fetchMakeAndModel()
    return render_template("computers.html", data=data)


@views.route('/monitors')
def monitors():
    data = fetchMakeAndModel()
    return render_template("monitors.html", data=data)


@views.route('/printers')
def printers():
    data = fetchMakeAndModel()
    return render_template("printers.html", data=data)


@views.route('/network')
def network():
    data = fetchMakeAndModel()
    return render_template("network.html", data=data)


@views.route('/cartridges')
def cartridges():
    data = fetchMakeAndModel()
    print(data)
    return render_template("cartridges.html", data=data)


@views.route('/addCon', methods=['GET', 'POST'])
def addCon():
    amount = int(request.form.get('amount'))
    model = request.form.get('model')
    modelname = model.split()[1]
    from .db_connect import connect_sql
    conx = connect_sql()
    query = 'update dbo.consumable SET amount += ? where dbo.consumable.name = ?'
    cursor = conx.cursor()
    cursor.execute(query, amount, modelname)
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
    cons = (model, 'Cartridge', amount)
    global consumables, Gdate
    consumables.append(cons)
    Gdate = date

    return redirect('/cartridges')


@views.route('/addComputer', methods=['GET', 'POST'])
def addComputer():
    snumber = request.form.get('snumber')
    makeAndModel = request.form.get('model')
    category1 = request.form.get('category')
    condition1 = request.form.get('condition')
    condition = 0
    category = 0
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
    modelname = makeAndModel.split()[1]
    from .db_connect import connect_sql
    conx = connect_sql()
    modelquery = 'select id from dbo.model where dbo.model.name = ?'
    query = 'insert into hardware(serialNumber, categoryId, makeAndModel, condition) values (?,?,?,?)'
    cursor = conx.cursor()
    cursor.execute(modelquery, modelname)
    modelId = cursor.fetchall()[0][0]
    cursor.execute(query, snumber, category, modelId, condition)
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
    addToCart(snumber)
    global Gdate
    Gdate = date
    return redirect('/computers')


@views.route('/addMonitor', methods=['GET', 'POST'])
def addMonitor():
    snumber = request.form.get('snumber')
    makeAndModel = request.form.get('model')
    condition1 = request.form.get('condition')
    condition = 0
    category = 5
    if condition1 == 'New':
        condition = 1
    elif condition1 == 'Used':
        condition = 2
    else:
        condition = 3
    modelname = makeAndModel.split()[1]
    from .db_connect import connect_sql
    conx = connect_sql()
    modelquery = 'select id from dbo.model where dbo.model.name = ?'
    query = 'insert into hardware(serialNumber, categoryId, makeAndModel, condition) values (?,?,?,?)'
    cursor = conx.cursor()
    cursor.execute(modelquery, modelname)
    modelId = cursor.fetchall()[0][0]
    cursor.execute(query, snumber, category, modelId, condition)
    conx.commit()
    conx.close()
    return redirect('/monitors')


@views.route('/issueMonitor', methods=['GET', 'POST'])
def issueMonitor():
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
    addToCart(snumber)
    global Gdate
    Gdate = date
    return redirect('/monitors')


@views.route('/addPrinter', methods=['GET', 'POST'])
def addPrinter():
    snumber = request.form.get('snumber')
    makeAndModel = request.form.get('model')
    condition1 = request.form.get('condition')
    condition = 0
    category = 6
    if condition1 == 'New':
        condition = 1
    elif condition1 == 'Used':
        condition = 2
    else:
        condition = 3
    modelname = makeAndModel.split()[1]
    from .db_connect import connect_sql
    conx = connect_sql()
    modelquery = 'select id from dbo.model where dbo.model.name = ?'
    query = 'insert into hardware(serialNumber, categoryId, makeAndModel, condition) values (?,?,?,?)'
    cursor = conx.cursor()
    cursor.execute(modelquery, modelname)
    modelId = cursor.fetchall()[0][0]
    cursor.execute(query, snumber, category, modelId, condition)
    conx.commit()
    conx.close()
    return redirect('/printers')


@views.route('/issuePrinter', methods=['GET', 'POST'])
def issuePrinter():
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
    addToCart(snumber)
    global Gdate
    Gdate = date
    return redirect('/printers')


@views.route('/addNetwork', methods=['GET', 'POST'])
def addNetwork():
    snumber = request.form.get('snumber')
    makeAndModel = request.form.get('model')
    condition1 = request.form.get('condition')
    condition = 0
    catname = request.form.get('category')
    if condition1 == 'New':
        condition = 1
    elif condition1 == 'Used':
        condition = 2
    else:
        condition = 3
    modelname = makeAndModel.split()[1]
    from .db_connect import connect_sql
    conx = connect_sql()
    modelquery = 'select id from dbo.model where dbo.model.name = ?'
    catquery = 'select id from dbo.consumableCat where dbo.consumableCat.name = ?'
    query = 'insert into hardware(serialNumber, categoryId, makeAndModel, condition) values (?,?,?,?)'
    cursor = conx.cursor()
    cursor.execute(modelquery, modelname)
    modelId = cursor.fetchall()[0][0]
    cursor.execute(catquery, catname)
    category = cursor.fetchall()[0][0]
    cursor.execute(query, snumber, category, modelId, condition)
    conx.commit()
    conx.close()
    return redirect('/network')


@views.route('/issueNetwork', methods=['GET', 'POST'])
def issueNetwork():
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
    addToCart(snumber)
    global Gdate
    Gdate = date
    return redirect('/network')


@views.route('/searchClients', methods=['GET', 'POST'])
def searchClients():
    useremail = request.form.get('user')
    getuserId = 'select id from dbo.clients where email = ?'
    query = 'SELECT dbo.hardware.serialNumber, dbo.hardware.receiveDate, dbo.model.name, dbo.consumableCat.name from dbo.hardware INNER JOIN dbo.model on dbo.hardware.makeAndModel = dbo.model.id INNER JOIN dbo.consumableCat on dbo.hardware.categoryId = dbo.consumableCat.id where dbo.hardware.userId = ? order by dbo.hardware.receiveDate asc;'
    from .db_connect import connect_sql
    conx = connect_sql()
    cursor = conx.cursor()
    cursor.execute(getuserId, useremail)
    data = cursor.fetchall()
    userId = data[0][0]
    cursor.execute(query, userId)
    data = cursor.fetchall()
    global results
    results = data
    return render_template('/clients.html', data=data)


@views.route('/print')
def printForm():
    global hardware, Gdate
    print(hardware)
    items = hardware
    hardware = []
    global consumables
    items2 = consumables
    consumables = []
    print(items)
    return render_template('/receipt.html', data=items, consume=items2, date=Gdate)
