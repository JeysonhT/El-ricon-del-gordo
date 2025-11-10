from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..data.mysqlConexion import get_db

admin_ct = Blueprint("admin", __name__)


@admin_ct.route("/admin")
def admin_dashboard():
    if "islogued" in session and session.get("id_role") == 2:
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("select count(*) as countUser FROM usuario")
            usersCount = cursor.fetchone()
            cursor.execute("SELECT COUNT(*) as count FROM productos")
            productsCount = cursor.fetchone()
            cursor.close()
            return render_template("admin.html", userCount=usersCount, productsCount=productsCount, user=session.get("email"))
        except Exception as e:
            flash("An error occurred while loading the admin dashboard.", "error")
            return render_template("error.html", code=500, message=e)
    else:
        flash("Access denied. Admins only.", "error")
        return redirect(url_for("login.sigin"))
