from flask import Blueprint
from .users import users_bp

# Stubs — filled in Tasks 4 and 5
projects_bp = Blueprint("projects", __name__, url_prefix="/api/projects")
tasks_bp = Blueprint("tasks", __name__, url_prefix="/api/tasks")


def register_blueprints(app):
    app.register_blueprint(users_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(tasks_bp)
