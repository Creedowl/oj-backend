from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.user import user_get, user_add, user_update
from app.models.user import User
from app.schemas.user import UserCreate, UserDB, UserInfo, UserUpdate
from app.utils.security import get_current_user

router = APIRouter()


@router.post("/register", response_model=UserInfo)
def register(
        *,
        db: Session = Depends(get_db),
        user_in: UserCreate
):
    user = user_get(db, student_id=user_in.student_id)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this student id already exists in the system"
        )
    user = user_add(db, user_in)
    return user


@router.get("/{user_id}", response_model=UserInfo)
def user_info(
        *,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user),
        user_id: int
):
    if user_id == user.id:
        return user
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission deny"
        )
    u = user_get(db, user_id)
    if u is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return u


@router.post("/{user_id}", response_model=UserInfo)
def update_user(
        *,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user),
        user_id: int,
        update: UserUpdate
):
    if user_id != user.id:
        if not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission deny"
            )
        user = user_get(db, user_id=user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
    try:
        return user_update(db, user, update)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
