from app.models.user_role import UserRole


class User:
    def __init__(self, id=None, name=None, email=None, role: UserRole = UserRole.MEMBER, password=None):
        self.id = id
        self.name = name
        self.email = email
        self.role = role
        self.password = password

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role.value,
        }