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
