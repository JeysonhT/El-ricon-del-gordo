from flask import Blueprint, flash, render_template, request, redirect, url_for, session
from ..Services.UserServices import UserService
from ..models.Users import User

user_ct = Blueprint("user", __name__)

service = UserService()


def form_validator(email, name, password, id_role):
    if email and name and password and id_role:
        return True
    return False


@user_ct.route("/users")
def get_users():
    if "islogued" in session:
        users = service.obtener_usarios()

        if users:
            return render_template("users.html", users=users)
        else:
            flash("No hay usuarios registrados!!", "ERROR")
            return redirect(url_for("admin.admin_dashboard"))
    else:
        flash("Access denied. Please log in.", "error")
        return redirect(url_for("login.sigin"))


@user_ct.route("/create-user", methods=["POST"])
def create_user():
    if "islogued" in session:
        try:
            email = request.form.get("email")
            password = request.form.get("password")
            name = request.form.get("name")
            role = request.form.get("role")

            if form_validator(email, password, name, role):
                new_user = User(
                    _id_user=None,
                    _email=email,
                    _password=password,
                    _name=name,
                    _id_role=role,
                )
                service.crear_usuario(new_user)
                flash("Usuario creado correctamente", "success")
            else:
                flash("Todos los campos son requeridos.", "error")
        except Exception as e:
            flash(f"Error al crear el usuario: {e}", "error")

        return redirect(url_for("user.get_users"))
    else:
        flash("Access denied. Please log in.", "error")
        return redirect(url_for("login.sigin"))


@user_ct.route("/update-user", methods=["POST"])
def update_user():
    if "islogued" in session:
        try:
            user_id = request.form.get("user_id")
            email = request.form.get("email")
            password = request.form.get("password")
            name = request.form.get("name")
            role = request.form.get("role")

            # 1. Obtener el usuario existente
            user = service.obtener_usuario_id(id_user=user_id)

            if not user:
                flash("Usuario no encontrado", "error")
                return redirect(url_for("user.get_users"))

            # 2. Decidir qué contraseña usar
            if password:
                # Si se proporciona una nueva contraseña, úsala
                password_to_use = password
            else:
                # Si no, mantén la contraseña antigua
                password_to_use = user.password

            # 3. Validar los datos del formulario
            if email and name and role:
                updated_user = User(
                    _id_user=user_id,
                    _email=email,
                    _name=name,
                    _password=password_to_use,
                    _id_role=role,
                )
                # 4. Llamar al servicio con el objeto correcto
                service.actualizar_usuario(updated_user)
                flash("Usuario actualizado correctamente", "success")
            else:
                flash("Faltan datos en el formulario", "error")

        except Exception as e:
            flash(f"Error al actualizar el usuario: {e}", "error")
            import traceback

            traceback.print_exc()

        return redirect(url_for("user.get_users"))
    else:
        flash("Access denied. Please log in.", "error")
        return redirect(url_for("login.sigin"))


@user_ct.route("/eliminar_usuario/<int:id>", methods=["POST"])
def eliminar_usuario(id: int):
    if id > 0:
        service.borrar_usuario(id)
        flash("Usuario Borrado", "Success")
        return redirect(url_for("user.get_users"))

    flash("Error al borrar el usuario, el id es incorrecto", "Error")
    return redirect(url_for("user.get_users"))


# Lista de contactos
contacts = [
    {"nombre": "Maria", "numero": 67890656, "correo": "maria@example.com"},
    {"nombre": "Luis", "numero": 89897656, "correo": "Luis@example.com"},
    {"nombre": "Petrona", "numero": 87324567, "correo": "Petrona@example.com"},
]


@user_ct.route("/contacts", methods=["GET", "POST"])
def manage_contacts():
    if request.method == "POST":
        contact = {
            "nombre": request.form.get("nombre"),
            "numero": request.form.get("numero"),
            "correo": request.form.get("correo"),
        }
        contacts.append(contact)

    return render_template("contact.html", contacts=contacts)


@user_ct.route("/delete-contact", methods=["POST"])
def delete_contact():
    nombre = request.form.get("nombre")

    global contacts
    contacts = [contact for contact in contacts if contact["nombre"] != nombre]

    return redirect(url_for("user.manage_contacts"))
