from app.models import User, Project, Task


def test_user_creation(db):
    user = User(name="Alice", email="alice@beacon.dev")
    db.session.add(user)
    db.session.commit()
    assert user.id is not None
    assert user.name == "Alice"


def test_project_creation(db):
    project = Project(name="Infra", description="Infrastructure tasks")
    db.session.add(project)
    db.session.commit()
    assert project.id is not None


def test_task_creation(db):
    user = User(name="Bob", email="bob@beacon.dev")
    project = Project(name="Backend")
    db.session.add_all([user, project])
    db.session.flush()

    task = Task(
        title="Write tests",
        status="todo",
        assignee_id=user.id,
        project_id=project.id,
    )
    db.session.add(task)
    db.session.commit()
    assert task.id is not None
    assert task.status == "todo"
