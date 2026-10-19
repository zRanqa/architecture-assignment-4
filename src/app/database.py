from app.errors import NotFoundError
from app.models.equipment_status import EquipmentStatus
from app.models.farm import Farm
from app.models.task import Task
from app.models.task_status import TaskStatus
from app.models.user import User
from app.models.equipment import Equipment
from app.models.user_role import UserRole

class Database:
    def __init__(self):
        members = [
            User(1, "Bob", "bob@email.com", UserRole.ADMIN),
            User(2, "Fred", "fred@email.com", UserRole.ADMIN),
            User(3, "Alice", "alice@email.com", UserRole.MEMBER),
            User(4, "Jim", "jim@email.com", UserRole.MEMBER)
        ]
        equipment = [
            Equipment(1, "Soil pH Meter", EquipmentStatus.ACTIVE),
            Equipment(2, "Soil Moisture Sensor", EquipmentStatus.ACTIVE),
            Equipment(3, "Weather Station", EquipmentStatus.ACTIVE),
            Equipment(4, "Rain Gauge", EquipmentStatus.ACTIVE),
            Equipment(5, "EC (Electrical Conductivity) Meter", EquipmentStatus.MAINTENANCE),
            Equipment(6, "Handheld Refractometer", EquipmentStatus.ACTIVE),
            Equipment(7, "Tractor", EquipmentStatus.INACTIVE),
        ]
        tasks = [
            Task(1, "Weeding", "Weed the farm", TaskStatus.COMPLETED, due_date="17/12/2026", equipment=[equipment[2]], assigned_members=[members[0], members[1]]),
            Task(2, "Soil pH Testing", "Test pH levels across all paddocks", TaskStatus.COMPLETED, due_date="05/11/2026", equipment=[equipment[0]], assigned_members=[members[2]]),
            Task(3, "Irrigation Check", "Check soil moisture before scheduling irrigation", TaskStatus.COMPLETED, due_date="10/11/2026", equipment=[equipment[1]], assigned_members=[members[3], members[0]]),
            Task(4, "Rainfall Logging", "Record weekly rainfall totals", TaskStatus.IN_PROGRESS, due_date="25/10/2026", equipment=[equipment[3]], assigned_members=[members[1]]),
            Task(5, "Weather Monitoring", "Review wind and temperature data for spraying window", TaskStatus.IN_PROGRESS, due_date="30/10/2026", equipment=[equipment[2]], assigned_members=[members[2], members[3]]),
            Task(6, "Fertiliser Planning", "Adjust fertiliser plan based on pH and conductivity results", TaskStatus.IN_PROGRESS, due_date="02/11/2026", equipment=[equipment[0], equipment[4]], assigned_members=[members[0], members[2]]),
            Task(7, "Salinity Testing", "Measure soil salinity in the lower paddock", TaskStatus.TO_BE_STARTED, due_date="15/11/2026", equipment=[equipment[4]], assigned_members=[members[3]]),
            Task(8, "Harvest Sugar Check", "Check fruit sugar levels before harvest", TaskStatus.TO_BE_STARTED, due_date="20/11/2026", equipment=[equipment[5]], assigned_members=[members[1], members[2]]),
            Task(9, "Ploughing", "Plough the north paddock ahead of planting", TaskStatus.TO_BE_STARTED, due_date="01/12/2026", equipment=[equipment[6]], assigned_members=[members[0]]),
            Task(10, "Equipment Calibration", "Calibrate all soil sensors", TaskStatus.UNASSIGNED, due_date="10/12/2026", equipment=[equipment[0], equipment[1], equipment[4]]),
            Task(11, "Fence Inspection", "Walk the boundary and note any repairs needed", TaskStatus.UNASSIGNED, due_date="14/12/2026"),
            Task(12, "Seasonal Soil Survey", "Full moisture and pH survey for next season's planning", TaskStatus.UNASSIGNED, due_date="20/12/2026", equipment=[equipment[0], equipment[1]]),
        ]
        self.farm = Farm(
            1, members=members, tasks=tasks, equipment=equipment
        )

    def get_farm_members(self, filter_roles):
        return [m for m in self.farm.members if filter_roles[m.role.value]]

    def add_member(self, new_user: User):
        new_id = 0
        for i in self.farm.members:
            if i.id > new_id:
                new_id = i.id

        new_user.id = new_id + 1

        self.farm.members.append(new_user)

        return new_user

    def get_unassigned_tasks(self):
        return [t for t in self.farm.tasks if t.status == TaskStatus.UNASSIGNED]

    def get_equipment(self):
        return self.farm.equipment

    def add_task(self, new_task):
        new_id = 0
        for i in self.farm.tasks:
            if i.id > new_id:
                new_id = i.id

        new_task.id = new_id + 1

        self.farm.tasks.append(new_task)

        return new_task

    def get_task(self, task_id):
        return next((t for t in self.farm.tasks if t.id == task_id), None)

    def assign_task(self, task_id, member_ids):
        task = db.get_task(task_id)
        if task is None:
            raise NotFoundError(f'Could not find task by id: {task_id}')
        members = [m for m in self.farm.members if m.id in member_ids and m not in task.assigned_members]

        task.assigned_members.extend(members)
        if task.status == TaskStatus.UNASSIGNED:
            task.status = TaskStatus.TO_BE_STARTED
        return task


    def get_tasks_from_member(self, member_id, completed, in_progress, to_be_started):
        return [t for t in self.farm.tasks if member_id in [id.id for id in t.assigned_members] and (
            completed and (t.status == TaskStatus.COMPLETED) or 
            in_progress and (t.status == TaskStatus.IN_PROGRESS) or 
            to_be_started and (t.status == TaskStatus.TO_BE_STARTED)
        )]

    def get_member_role(self, member_id):
        for i in self.farm.members:
            if i.id == member_id:
                return i.role

    def update_task_status(self, task_id, new_status):
        task = db.get_task(task_id)
        if task is None:
            raise NotFoundError(f'Could not find task by id: {task_id}')

        task.status = new_status
        return task

    def update_task(self, task_id, new_status, new_title, new_description, new_due_date):
        task = db.get_task(task_id)
        if task is None:
            raise NotFoundError(f'Could not find task by id: {task_id}')

        task.status = new_status
        task.title = new_title
        task.due_date = new_due_date
        task.description = new_description
        return task

    def delete_task(self, task_id):
        task = db.get_task(task_id)
        if task is None:
            raise NotFoundError(f'Could not find task by id: {task_id}')

        self.farm.tasks = [t for t in self.farm.tasks if t.id != task_id]


        


    
db = Database()