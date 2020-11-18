from typing import Optional

from sqlalchemy.orm import Session

from app.db.classU import class_get
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.utils.security import verify_password, hash_password


# verify password
def user_authenticate(db: Session, student_id: str, password: str) -> Optional[User]:
    user = db.query(User).filter(User.student_id == student_id).first()
    if not user:
        return None
    if not verify_password(user.student_id, password, user.hashed_password):
        raise Exception("Password is wrong")
    return user


# get a user
def user_get(db: Session, user_id: int = 0, student_id: str = None) -> Optional[User]:
    fil = []
    if user_id != 0:
        fil.append(User.id == user_id)
    if student_id is not None:
        fil.append(User.student_id == student_id)
    user = db.query(User).filter(*fil).first()
    if not user:
        return None
    return user


# remember to check if the user exists first
def user_add(db: Session, user_in: UserCreate) -> User:
    user = User(
        name=user_in.name,
        student_id=user_in.student_id,
        hashed_password=hash_password(user_in.student_id, user_in.password),
        is_admin=False
    )
    # TODO: Exception handler
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def user_update(db: Session, user: User, update: UserUpdate) -> User:
    # update class
    class_id = update.classU_id
    if class_id is None or class_id is 0:
        class_id = None
    else:
        # check whether class exists
        if class_get(db, class_id) is None:
            raise Exception("Class {} not found".format(class_id))
    user.classU_id = class_id

    # update password
    if update.new_password is not None:
        if not user.is_admin and \
                update.old_password is not None and \
                not verify_password(user.student_id, update.old_password, user.hashed_password):
            raise Exception("Password is wrong")
        user.hashed_password = hash_password(user.student_id, update.new_password)
    db.commit()
    db.refresh(user)
    return user


def user_set_class(db: Session, user: User, class_id: Optional[int]) -> User:
    user.classU_id = class_id
    db.commit()
    db.refresh(user)
    return user
