from app.models.user import User
from app.models.task import Task
from app.models.equipment import Equipment

class Farm:
    def __init__(self, id = None, members: list[User] = [], tasks: list[Task] = [], equipment: list[Equipment] = []):
        self.id = id
        self.members = members
        self.tasks = tasks
        self.equipment = equipment
