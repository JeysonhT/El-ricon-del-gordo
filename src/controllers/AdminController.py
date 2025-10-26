from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..data.mysqlConexion import get_db

admin_ct = Blueprint("admin", __name__)


@admin_ct.route("/admin")
def admin_dashboard():
    if "islogued" in session and session.get("id_role") == 2:
        return render_template("admin.html", user=session.get("email"))
    else:
        flash("Access denied. Admins only.", "error")
        return redirect(url_for("login.sigin"))
