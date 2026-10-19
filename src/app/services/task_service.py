from flask import jsonify
from app.database import db
from app.errors import ValidationError, ForbiddenError
from app.models.task_status import TaskStatus
from app.models.user_role import UserRole
from app.utils import utils
from app.models.task import Task
from app.services import equipment_service


def get_all_unassigned_tasks():
    return db.get_unassigned_tasks()

def add_task(request_json):
    utils.validate_request_json(request_json, ("equipment_ids", "title", "description", "due_date"))
    equipment = equipment_service.get_equipment_by_ids(request_json["equipment_ids"])
    
    due_date = utils.validate_date_string(request_json["due_date"], "due_date")
    due_date = request_json["due_date"]
    new_task = Task(
        None,
        request_json["title"],
        request_json["description"],
        TaskStatus.UNASSIGNED,
        due_date,
        equipment,
        []
    )
    return db.add_task(new_task)

def assign_task(request_json):
    utils.validate_request_json(request_json, ("task_id", "member_ids"))
    task_id = request_json["task_id"]
    member_ids = request_json["member_ids"]
    return db.assign_task(task_id, member_ids)

def get_all_member_tasks(member_id, request_json):

    utils.validate_request_json(request_json, ("completed", "in progress", "to be started"))
    
    completed = request_json[TaskStatus.COMPLETED.value]
    in_progress = request_json[TaskStatus.IN_PROGRESS.value]
    to_be_started = request_json[TaskStatus.TO_BE_STARTED.value]
    return db.get_tasks_from_member(member_id, completed, in_progress, to_be_started)


def update_task(member_id, task_id, request_json):
    
    utils.validate_request_json(request_json, ("status", ))

    new_status = utils.validate_string_to_enum(TaskStatus, request_json["status"], "status")

    member_role = db.get_member_role(member_id)
    if member_role == UserRole.ADMIN:
        utils.validate_request_json(request_json, ("status", "title", "description", "due_date"))

        new_title = request_json["title"]
        new_description = request_json["description"]

        # just validates the date string
        new_due_date = utils.validate_date_string(request_json["due_date"], "due_date")
        new_due_date = request_json["due_date"]

        return db.update_task(task_id, new_status, new_title, new_description, new_due_date)
    elif member_role == UserRole.MEMBER:
        return db.update_task_status(task_id, new_status)
    else:
        raise ValidationError("User is not an admin or member")

def delete_task(member_id, task_id):
    member_role = db.get_member_role(member_id)
    if member_role == UserRole.ADMIN:
        db.delete_task(task_id)
    elif member_role == UserRole.MEMBER:
        raise ForbiddenError("Only admins can delete tasks")
    else:
        raise ValidationError("User is not an admin or member")