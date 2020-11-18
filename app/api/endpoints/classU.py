from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.db.classU import class_get_all, class_create, class_get, class_delete
from app.db.database import get_db
from app.models.user import User
from app.schemas.classU import ClassUOut, ClassUInfo, ClassDelete, ClassCreate
from app.utils.security import get_current_user

router = APIRouter()


@router.get("/", response_model=List[ClassUOut])
def get_all_classes(
        db: Session = Depends(get_db),
        offset: int = 0,
        limit: int = 100
):
    return class_get_all(db, offset, limit)


@router.get("/{class_id}", response_model=ClassUInfo)
def get_class(*, db: Session = Depends(get_db), class_id: int):
    cls = class_get(db, class_id)
    if not cls:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="404 Not Found"
        )
    return cls


@router.post("/", response_model=ClassUOut)
def create_class(
        *,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user),
        class_in: ClassCreate):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="permission deny"
        )
    cl = class_create(db, class_in)
    if cl is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="class exists"
        )
    return cl


# @router.post("/join/{class_id}", response_model=UserDB)
# def class_join(
#         *,
#         db: Session = Depends(get_db),
#         user: User = Depends(get_current_user),
#         class_id: int
# ) -> User:
#     if class_id == 0:
#         return user_set_class(db, user, None)
#     else:
#         cl = class_get(db, class_id)
#         if cl is None:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="class not found"
#             )
#         return user_set_class(db, user, class_id)


@router.delete("/{class_id}", response_model=ClassDelete)
def delete_class(
        *,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user),
        class_id: int
):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="permission deny"
        )
    try:
        class_delete(db, class_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    return {
        'result': True
    }
