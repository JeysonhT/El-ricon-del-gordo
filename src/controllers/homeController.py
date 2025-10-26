from flask import Blueprint, flash, redirect, render_template, session, url_for

home_ct = Blueprint("home", __name__)


@home_ct.route("/")
def inicio():
    return render_template("index.html")


@home_ct.route("/index")
def index():
    email = session["email"]
    return render_template("index.html", email=email)


@home_ct.route("/perfil")
def perfil():
    if "islogued" in session and session.get("id_role") == 2:
        return render_template("perfil.html")
    else:
        flash("Access denied. Admins only.", "error")
        return redirect(url_for("login.sigin", email=session["email"]))
