from flask import Blueprint, request, jsonify
from ..services.project_service import (
    get_all_projects,
    get_project_by_id,
    create_project,
)

projects_bp = Blueprint("projects", __name__, url_prefix="/api/projects")


@projects_bp.route("", methods=["GET"])
def list_projects():
    projects = get_all_projects()
    return jsonify([p.to_dict() for p in projects]), 200


@projects_bp.route("", methods=["POST"])
def create_project_route():
    data = request.get_json() or {}
    name = data.get("name")
    if not name:
        return jsonify({"error": "name is required"}), 400
    project = create_project(name=name, description=data.get("description", ""))
    return jsonify(project.to_dict()), 201


@projects_bp.route("/<int:project_id>", methods=["GET"])
def get_project(project_id):
    project = get_project_by_id(project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404
    return jsonify(project.to_dict()), 200
