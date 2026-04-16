import pytest
from app import create_app
from app.database import db as _db


@pytest.fixture(scope="session")
def app():
    app = create_app({
        "TESTING": True,
        "PROPAGATE_EXCEPTIONS": False,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture(scope="function")
def db(app):
    with app.app_context():
        yield _db
        _db.session.rollback()
        # Truncate all tables so committed data doesn't bleed between tests
        for table in reversed(_db.metadata.sorted_tables):
            _db.session.execute(table.delete())
        _db.session.commit()


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()
