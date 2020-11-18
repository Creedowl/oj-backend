from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.token import TokenPayload
from app.utils import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(student_id: str, raw_password: str) -> str:
    return pwd_context.hash(student_id + raw_password + config.PASSWORD_SALT)


def verify_password(student_id: str, raw_password: str, hashed_password: str) -> bool:
    origin = student_id + raw_password + config.PASSWORD_SALT
    return pwd_context.verify(origin, hashed_password)


def generate_jwt(data: dict):
    data.update({"exp": datetime.utcnow() + timedelta(minutes=config.JWT_EXPIRE_SECONDS)})
    return jwt.encode(data, config.JWT_KEY, config.JWT_ALGORITHM)


# get the current logged in user
def get_current_user(
        db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = jwt.decode(token, config.JWT_KEY, algorithms=config.JWT_ALGORITHM)
        data = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    user = db.query(User).filter(User.student_id == data.sub).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
