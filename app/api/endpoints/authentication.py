from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.user import user_authenticate
from app.schemas.token import Token
from app.utils.security import hash_password, generate_jwt

router = APIRouter()


@router.post("/login", response_model=Token)
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
            detail=hash_password(form_data.username, form_data.password),
            headers={"WWW-Authenticate": "Bearer"}
        )
    return {"access_token": generate_jwt({"sub": user.student_id}), "token_type": "bearer"}
