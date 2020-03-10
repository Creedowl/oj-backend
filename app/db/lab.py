from typing import Optional, List

from sqlalchemy.orm import Session

from app.models.lab import Lab
from app.schemas.lab import LabIn


def lab_get(db: Session, lab_id: int) -> Optional[Lab]:
    return db.query(Lab).filter(Lab.id == lab_id).first()


def lab_get_all(db: Session, offset: int = 0, limit: int = 100) -> List[Lab]:
    return db.query(Lab).offset(offset).limit(limit).all()


def lab_create(db: Session, lab_in: LabIn) -> Lab:
    lab = Lab(**lab_in.dict())
    # TODO: Exception handler
    db.add(lab)
    db.commit()
    db.refresh(lab)
    return lab
