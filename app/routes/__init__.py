from .users import users_bp
from .projects import projects_bp
from .tasks import tasks_bp


def register_blueprints(app):
    app.register_blueprint(users_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(tasks_bp)
