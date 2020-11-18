from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.lab import lab_get_all, lab_get, lab_create
from app.models.user import User
from app.schemas.lab import LabOut, LabIn
from app.utils.security import get_current_user

router = APIRouter()


@router.get("/", response_model=List[LabOut])
def get_all_labs(
        db: Session = Depends(get_db),
        offset: int = 0,
        limit: int = 100
):
    return lab_get_all(db, offset, limit)


@router.get("/{lab_id}", response_model=LabOut)
def get_lab(*, db: Session = Depends(get_db), lab_id: int):
    lab = lab_get(db, lab_id)
    if not lab:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="404 Not Found"
        )
    return lab


@router.post("/", response_model=LabOut)
def create_lab(
        *,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user),
        lab_in: LabIn
):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission deny"
        )
    return lab_create(db, lab_in)
