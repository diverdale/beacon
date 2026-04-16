from ..database import db
from ..models import Project


def get_all_projects():
    return Project.query.all()


def get_project_by_id(project_id):
    return db.session.get(Project, project_id)


def create_project(name, description=""):
    project = Project(name=name, description=description)
    db.session.add(project)
    db.session.commit()
    return project
