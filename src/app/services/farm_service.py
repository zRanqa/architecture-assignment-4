from flask import jsonify
from app.database import db
from app.errors import ValidationError
from app.models.user import User
from app.models.task import Task
from app.models.task_status import TaskStatus
from app.utils import utils
from app.models.user_role import UserRole

def get_all_members(request_json):

    utils.validate_request_json(request_json, ("roles",))

    roles = request_json["roles"]
    utils.validate_request_json(roles, ("admin", "member"), missing_message="in roles")
            
    filter_roles = {
        "admin": roles["admin"],
        "member": roles["member"]
    }
    return db.get_farm_members(filter_roles)

def add_member(request_json):
    utils.validate_request_json(request_json, ("name", "email", "role", "password"))

    role = utils.validate_string_to_enum(UserRole, request_json["role"], "role")

    new_user = User(None, request_json["name"], request_json["email"], role, request_json["password"])
    return db.add_member(new_user)
