class User:

    def __init__(
        self,
        _id_user,
        _email: str,
        _password: str,
        _id_role: int,
        _name: str,
    ):
        self._id_user = _id_user
        self._email = _email
        self._password = _password
        self._id_role = _id_role
        self._name = _name

    @property
    def id_user(self) -> int:
        return self._id_user

    @property
    def email(self):
        return self._email

    @property
    def password(self):
        return self._password

    @property
    def name(self):
        return self._name

    @property
    def id_role(self) -> int:
        return self._id_role

    @id_user.setter
    def id_user(self, _id_user: int):
        self._id_user = _id_user

    @email.setter
    def email(self, _email: str):
        self._email = _email

    @password.setter
    def password(self, _password: str):
        self._password = _password

    @name.setter
    def name(self, _name: str):
        self._name = _name

    @id_role.setter
    def id_role(self, _id_role: int):
        self._id_role = _id_role
