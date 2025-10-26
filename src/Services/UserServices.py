import traceback
from ..data.mysqlConexion import get_db
from ..models.Users import User


class UserService:

    def crear_usuario(self, user: User):
        try:
            db = get_db()
            cursor = db.cursor()

            print("AQUI ESTA EL DATO QUE BUSCAS: ", user.email)

            args = (user.email, user.password, user.id_role, user.name)

            cursor.callproc("CrearUsuario", args)
            db.commit()
        except Exception as e:
            print(f"Error al crear el usuario: {e}")

    def actualizar_usuario(self, user: User):
        try:
            db = get_db()
            cursor = db.cursor()

            print("AQUI ESTA EL DATO QUE BUSCAS: ", user.id_role)

            args = (
                user.id_user,
                user.email,
                user.password,
                user.name,
                user.id_role,
            )

            cursor.callproc("ActualizarUsuario", args)
            db.commit()

        except Exception as e:
            print(f"error al actualizar el usuario: {e}")

    def borrar_usuario(self, id_usuario: int):
        try:
            db = get_db()
            cursor = db.cursor()

            cursor.callproc("EliminarUsuario", (id_usuario,))

            db.commit()

        except Exception as e:
            print(f"Error al eliminar el usuario: {e}")

    def obtener_usarios(self) -> list:
        try:
            db = get_db()
            cursor = db.cursor()

            cursor.execute("SELECT * FROM usuario")

            usuarios = cursor.fetchall()

            return usuarios
        except Exception as e:
            print(f"Error al obtener los usuarios: {e}")

        return []

    def obtener_usuario_id(self, id_user: int) -> User:
        try:
            db = get_db()
            cursor = db.cursor()

            cursor.execute("SELECT * FROM usuario WHERE id_user = %s", (id_user,))

            registry = cursor.fetchone()

            if registry:

                user = User(
                    registry["id_user"],
                    registry["email"],
                    registry["password"],
                    registry["id_role"],
                    registry["name"],
                )

                return user

        except Exception as e:
            print(f"Error al obtener el usuario: {e}")
            traceback.print_exc()

        return None
