from datetime import datetime, timezone
from ..database import db
from ..models import Task, Project


def get_all_tasks():
    return Task.query.all()


def get_task_by_id(task_id):
    return db.session.get(Task, task_id)


def create_task(title, project_id=None, assignee_id=None, description="", due_date=None):
    task = Task(
        title=title,
        description=description,
        project_id=project_id,
        assignee_id=assignee_id,
        due_date=due_date,
    )
    db.session.add(task)
    db.session.commit()
    return task


def update_task(task_id, **kwargs):
    task = db.session.get(Task, task_id)
    if not task:
        return None
    for key, value in kwargs.items():
        if hasattr(task, key):
            setattr(task, key, value)
    db.session.commit()
    return task


def delete_task(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        return False
    db.session.delete(task)
    db.session.commit()
    return True


# BUG 1: Filters by Project.name instead of Task.project_id.
# Symptom: returns tasks from projects with matching names across all projects,
# silently ignores numeric project_id. AI hallucinated the ORM join incorrectly.
def get_tasks_by_project(project_id):
    return (
        Task.query.join(Project)
        .filter(Project.name == project_id)  # should be Task.project_id == project_id
        .all()
    )


# BUG 2: No status transition validation.
# Allows 'archived' -> 'in_progress', 'done' -> 'todo', etc.
# A real implementation would enforce valid transitions.
def update_task_status(task_id, new_status):
    task = db.session.get(Task, task_id)
    if not task:
        return None
    task.status = new_status  # missing: validate new_status in Task.VALID_STATUSES
    if new_status == "done":
        task.completed_at = datetime.now(timezone.utc)
    db.session.commit()
    return task


# BUG 3: is_overdue uses strict > instead of >= for same-day due dates.
# Tasks due today are reported as not overdue until tomorrow.
def is_overdue(task):
    if not task.due_date or task.status in ("done", "archived"):
        return False
    return datetime.now(timezone.utc) > task.due_date  # should be >=
