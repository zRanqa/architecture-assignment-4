from app.models.equipment_status import EquipmentStatus


class Equipment:
    def __init__(self, id=None, name=None, status: EquipmentStatus | None = None):
        self.id = id
        self.name = name
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status.value
        }

