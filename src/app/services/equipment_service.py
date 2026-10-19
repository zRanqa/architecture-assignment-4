from app.database import db

def get_equipment_by_ids(equipment_ids):
    return [e for e in db.get_equipment() if e.id in equipment_ids]

def add_new_equipment():
    pass

def update_equipment():
    pass