from flask import Blueprint, render_template, redirect

home_ct = Blueprint("home", __name__)

@home_ct.route('/')
def inicio():
    return render_template("index.html")

@home_ct.route('/index')
def index():
    return render_template("index.html")