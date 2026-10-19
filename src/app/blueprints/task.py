from flask import Blueprint, jsonify, request
from app.services import task_service

task_bp = Blueprint("task", __name__, url_prefix="/<int:member_id>/tasks")

@task_bp.get("/")
def get_tasks(member_id):
    tasks = task_service.get_all_member_tasks(member_id, request.json)
    return jsonify([t.to_dict() for t in tasks])


@task_bp.put("/<int:task_id>/update")
def update_task(member_id, task_id):
    task = task_service.update_task(member_id, task_id, request.json)
    return jsonify(task.to_dict())

@task_bp.delete("/<int:task_id>/delete")
def delete_task(member_id, task_id):
    task_service.delete_task(member_id, task_id)
    return "", 204

# @task_bp.post("/add-member")
# def create_farm():
#     member = farm_service.add_member(request.json)
#     return jsonify(member.to_dict()), 201
