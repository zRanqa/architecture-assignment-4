from app.models.equipment import Equipment
from app.models.task_status import TaskStatus
from app.models.user import User

class Task:
    def __init__(self, id=None, title=None, description=None, status: TaskStatus | None = None, due_date=None, equipment: list[Equipment] | None = None, assigned_members: list[User] | None = None):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.due_date = due_date
        self.equipment = equipment if equipment is not None else []
        self.assigned_members = assigned_members if assigned_members is not None else []

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "due_date": self.due_date,
            "equipment": [e.to_dict() for e in self.equipment],
            "assigned_members": [m.to_dict() for m in self.assigned_members]
        }