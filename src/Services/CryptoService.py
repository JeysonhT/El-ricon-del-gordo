from werkzeug.security import generate_password_hash, check_password_hash


class PasswordService:
    """
    Un servicio para manejar el hashing y la verificación de contraseñas de forma segura.
    Utiliza werkzeug.security para generar y comprobar los hashes.
    """

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Genera un hash seguro para una contraseña.

        Args:
            password: La contraseña en texto plano.

        Returns:
            El hash de la contraseña, incluyendo el método y la sal.
        """
        if not isinstance(password, str) or not password:
            raise ValueError("La contraseña no puede estar vacía.")

        return generate_password_hash(password).encode("utf-8")

    @staticmethod
    def check_password(hashed_password: str, password: str) -> bool:
        """
        Verifica si una contraseña en texto plano coincide con un hash existente.

        Args:
            hashed_password: El hash de la contraseña almacenado.
            password: La contraseña en texto plano a verificar.

        Returns:
            True si la contraseña es correcta, False en caso contrario.
        """
        if not all(isinstance(arg, str) for arg in [hashed_password, password]):
            return False

        return check_password_hash(hashed_password, password)
