from .views import fetchDepartments
from flask import Blueprint, render_template, request, jsonify, flash
from flask.globals import session
from flask.helpers import url_for
from werkzeug.utils import redirect
from .db_connect import connect_sql


admin = Blueprint('admin', __name__)
