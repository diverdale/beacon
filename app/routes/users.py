from flask import Blueprint, request, jsonify
from ..services.user_service import (
    get_all_users,
    get_user_by_id,
    create_user,
    delete_user,
)

users_bp = Blueprint("users", __name__, url_prefix="/api/users")


@users_bp.route("", methods=["GET"])
def list_users():
    users = get_all_users()
    return jsonify([u.to_dict() for u in users]), 200


@users_bp.route("", methods=["POST"])
def create_user_route():
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "name and email are required"}), 400

    try:
        user = create_user(name=name, email=email)
    except ValueError as e:
        return jsonify({"error": str(e)}), 409

    return jsonify(user.to_dict()), 201


@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200


@users_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user_route(user_id):
    deleted = delete_user(user_id)
    if not deleted:
        return jsonify({"error": "User not found"}), 404
    return "", 204
