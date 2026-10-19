from flask import Blueprint, jsonify, request
from app.services import farm_service
from app.services import task_service

farm_bp = Blueprint("farm", __name__, url_prefix="/farm")

@farm_bp.get("/members")
def list_farms():
    members = farm_service.get_all_members(request.json)
    return jsonify([m.to_dict() for m in members])

@farm_bp.post("/add-member")
def create_farm():
    member = farm_service.add_member(request.json)
    return jsonify(member.to_dict()), 201


@farm_bp.get("/tasks")
def list_tasks():
    tasks = task_service.get_all_unassigned_tasks()
    return jsonify([task.to_dict() for task in tasks])


@farm_bp.post("/tasks/new")
def add_task():
    task = task_service.add_task(request.json)
    return jsonify(task.to_dict()), 201


@farm_bp.post("/tasks/assign")
def assign_task():
    task = task_service.assign_task(request.json)
    return jsonify(task.to_dict()), 201