from flask import Blueprint, request, jsonify
from ..services.task_service import (
    get_all_tasks,
    get_task_by_id,
    create_task,
    update_task,
    delete_task,
    update_task_status,
    get_tasks_by_project,
)

tasks_bp = Blueprint("tasks", __name__, url_prefix="/api/tasks")


@tasks_bp.route("", methods=["GET"])
def list_tasks():
    project_id = request.args.get("project_id", type=int)
    if project_id:
        tasks = get_tasks_by_project(project_id)
    else:
        tasks = get_all_tasks()
    return jsonify([t.to_dict() for t in tasks]), 200


@tasks_bp.route("", methods=["POST"])
def create_task_route():
    data = request.get_json() or {}
    title = data.get("title")
    if not title:
        return jsonify({"error": "title is required"}), 400

    task = create_task(
        title=title,
        project_id=data.get("project_id"),
        assignee_id=data.get("assignee_id"),
        description=data.get("description", ""),
    )
    return jsonify(task.to_dict()), 201


@tasks_bp.route("/<int:task_id>", methods=["GET"])
def get_task(task_id):
    # BUG (intentional): No None check — raises AttributeError (500) if not found
    # instead of returning 404 like the users blueprint does.
    task = get_task_by_id(task_id)
    return jsonify(task.to_dict()), 200


@tasks_bp.route("/<int:task_id>", methods=["PUT"])
def update_task_route(task_id):
    data = request.get_json() or {}
    task = update_task(task_id, **data)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task.to_dict()), 200


@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
def delete_task_route(task_id):
    deleted = delete_task(task_id)
    if not deleted:
        return jsonify({"error": "Task not found"}), 404
    return "", 204


@tasks_bp.route("/<int:task_id>/status", methods=["PATCH"])
def update_status(task_id):
    data = request.get_json() or {}
    status = data.get("status")
    if not status:
        return jsonify({"error": "status is required"}), 400
    task = update_task_status(task_id, status)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task.to_dict()), 200
