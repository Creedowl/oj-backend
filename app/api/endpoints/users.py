from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.user import user_get, user_add
from app.schemas.user import UserCreate, UserOut

router = APIRouter()


@router.post("/register", response_model=UserOut, response_model_exclude=["id"])
def register(
        *,
        db: Session = Depends(get_db),
        user_in: UserCreate
):
    user = user_get(db, user_in.student_id)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this student id already exists in the system"
        )
    user = user_add(db, user_in)
    return user
