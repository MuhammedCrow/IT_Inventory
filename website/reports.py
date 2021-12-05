from .views import fetchDepartments
from flask import Blueprint, render_template, request, jsonify, flash
from flask.globals import session
from flask.helpers import url_for
from werkzeug.utils import redirect
from .db_connect import connect_sql


reports = Blueprint('reports', __name__)


@reports.route('/cartridgeCons')
def cartridgeCons():
    depts = fetchDepartments()
    return render_template('consumption.html', depts=depts)


@reports.route('/searchDeptCons', methods=['POST'])
def searchDeptCons():
    headings = ('Cartridge', 'Amount')
    depts = fetchDepartments()
    dept = request.form.get('dept')
    startDate = request.form.get('startDate')
    endDate = request.form.get('endDate')
    getDeptId = 'select id from departments where name = ?'
    try:
        from .db_connect import connect_sql
        conx = connect_sql()
        cursor = conx.cursor()
        cursor.execute(getDeptId, dept)
        deptId = cursor.fetchone().id
        query = f"SELECT consumable.name, sum(consConsumption.amount) as amount from consConsumption INNER JOIN consumable on consConsumption.consId = consumable.id WHERE consConsumption.date >= '{startDate}' AND consConsumption.date < '{endDate}' AND consConsumption.deptId = {deptId} AND consConsumption.catId = 1 GROUP BY consumable.name"
        cursor.execute(query)
        data = cursor.fetchall()
        conx.close()
        return render_template('consumption.html', headings=headings, depts=depts, data=data)
    except Exception as e:
        flash(str(e), category='error')
    return render_template('consumption.html', headings=headings, depts=depts)
