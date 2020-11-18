from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.user import user_authenticate
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserOut
from app.utils.security import generate_jwt, get_current_user

router = APIRouter()


@router.post("/login", response_model=UserOut)
def login(
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 login part, use JWT as access token
    """
    try:
        user = user_authenticate(db, form_data.username, form_data.password)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
            # headers={"WWW-Authenticate": "Bearer"}
        )
    return {
        "access_token": generate_jwt({"sub": user.student_id}),
        "token_type": "bearer",
        **user.__dict__
    }


@router.post("/refresh", response_model=Token)
def refresh(user: User = Depends(get_current_user)):
    return {
        "access_token": generate_jwt({"sub": user.student_id}),
        "token_type": "bearer"
    }
