from flask import (
    render_template,
    request,
    Blueprint,
    current_app,
    flash,
    session,
    redirect,
    url_for,
)

from ..data.mysqlConexion import get_db
from ..Services.CryptoService import PasswordService

pass_service = PasswordService()

login_ct = Blueprint("login", __name__)


@login_ct.route("/sigin", methods=["GET", "POST"])
def sigin():
    if request.method == "POST":
        try:
            email = request.form.get("email")
            password = request.form.get("password")

            if not email or not password:
                return render_template(
                    "error.html",
                    code=400,
                    message="Email and password cannot be empty.",
                )

            db = get_db()
            cursor = db.cursor()
            args = (email,)
            cursor.execute("SELECT * FROM usuario WHERE email = %s", args)
            user = cursor.fetchone()
            cursor.close()

            if user:
                if pass_service.check_password(user["password"], password):
                    session["islogued"] = True
                    session["email"] = user["email"]
                    session["id_role"] = user["id_role"]

                    if user["id_role"] == 1:
                        return redirect(url_for("home.index"))
                    else:
                        return redirect(url_for("admin.admin_dashboard"))
                else:
                    flash("Email invalido o contraseña", "error")
                    # return render_template('error.html', code=401, message="Invalid email or password.")
        except Exception as e:
            current_app.logger.error(f"Error during login: {e}")
            return render_template(
                "error.html", code=500, message="Internal server error."
            )
    return render_template("login.html")


@login_ct.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        try:
            name = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")

            if not email or not password or not name:
                return render_template(
                    "error.html", code=400, message="All fields are required."
                )

            db = get_db()
            cursor = db.cursor()
            args = (email,)
            cursor.execute("SELECT * FROM usuario WHERE email = %s", args)
            existing_user = cursor.fetchone()

            if existing_user:
                cursor.close()
                return render_template(
                    "error.html", code=409, message="Email already registered."
                )

            hash_password = pass_service.hash_password(password=password)

            insert_args = (
                email,
                hash_password,
                1,
                name,
            )  # Assuming '1' is the default role ID for new users
            cursor.execute(
                "INSERT INTO usuario (email, password, id_role, name) VALUES (%s, %s, %s, %s)",
                insert_args,
            )
            db.commit()
            cursor.close()

            return render_template(
                "login.html", message="Registration successful. Please log in."
            )
        except Exception as e:
            current_app.logger.error(f"Error during registration: {e}")
            return render_template(
                "error.html", code=500, message="Internal server error."
            )

    return render_template("Registro.html")


@login_ct.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home.inicio"))
