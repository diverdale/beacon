from flask import Blueprint
from .users import users_bp
from .projects import projects_bp

# Stub — filled in Task 5
tasks_bp = Blueprint("tasks", __name__, url_prefix="/api/tasks")


def register_blueprints(app):
    app.register_blueprint(users_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(tasks_bp)
