from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import User
from app.utils.security import verify_password


# verify password
def user_authenticate(db: Session, student_id: str, password: str) -> Optional[User]:
    user = db.query(User).filter(User.student_id == student_id).first()
    if not user or not \
            verify_password(user.student_id, password, user.hashed_password):
        return None
    return user
