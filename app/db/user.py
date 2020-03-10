from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import verify_password, hash_password


# verify password
def user_authenticate(db: Session, student_id: str, password: str) -> Optional[User]:
    user = db.query(User).filter(User.student_id == student_id).first()
    if not user or not \
            verify_password(user.student_id, password, user.hashed_password):
        return None
    return user


# get a user by student id
def user_get(db: Session, student_id: str) -> Optional[User]:
    user = db.query(User).filter(User.student_id == student_id).first()
    if not user:
        return None
    return user


# remember to check if the user exists first
def user_add(db: Session, user_in: UserCreate) -> User:
    user = User(
        name=user_in.name,
        student_id=user_in.student_id,
        hashed_password=hash_password(user_in.student_id, user_in.password)
    )
    # TODO: Exception handler
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
