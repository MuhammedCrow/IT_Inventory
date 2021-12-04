from flask import Blueprint, render_template, request, jsonify, flash
from flask.globals import session
from flask.helpers import url_for
from werkzeug.utils import redirect
from .db_connect import connect_sql


reports = Blueprint('reports', __name__)

from .views import fetchDepartments
reports.route('/cartridgeCons')
def cartridgeCons():
    depts = fetchDepartments()
    headings = ('Cartridge', 'amount')
    return render_template('consumption.html', depts=depts, headings=headings)

reports.route('/searchDeptCons', methods=['POST'])
def searchDeptCons():
    dept = request.form.get('dept')
    startDate = request.form.get('startDate')
    endDate = request.form.get('endDate')
    query = 'SELECT '