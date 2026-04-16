from sqlalchemy.exc import IntegrityError
from ..database import db
from ..models import User


def get_all_users():
    return User.query.all()


def get_user_by_id(user_id):
    return db.session.get(User, user_id)


def create_user(name, email):
    user = User(name=name, email=email)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError(f"Email already in use: {email}")
    return user


def delete_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return False
    db.session.delete(user)
    db.session.commit()
    return True
