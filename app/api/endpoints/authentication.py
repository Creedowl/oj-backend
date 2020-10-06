from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.user import user_authenticate
from app.schemas.user import UserOut
from app.utils.security import generate_jwt

router = APIRouter()


@router.post("/login", response_model=UserOut)
def login(
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 login part, use JWT as access token
    """
    user = user_authenticate(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="user not found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return {
        "access_token": generate_jwt({"sub": user.student_id}),
        "token_type": "bearer",
        "name": user.name,
        "student_id": user.student_id,
        "is_admin": user.is_admin
    }
