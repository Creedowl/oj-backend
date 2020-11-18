from typing import Optional

from sqlalchemy.orm import Session

from app.models.classU import ClassU
from app.schemas.classU import ClassCreate


def class_get(db: Session, class_id: int) -> Optional[ClassU]:
    return db.query(ClassU).filter(ClassU.id == class_id).first()


def class_get_all(db: Session, offset: int = 0, limit: int = 100):
    return db.query(ClassU).offset(offset).limit(limit).all()


def class_create(db: Session, class_in: ClassCreate) -> Optional[ClassU]:
    cl = db.query(ClassU).filter(ClassU.name == class_in.name).first()
    if cl is not None:
        return None
    cl = ClassU(**class_in.dict())
    # TODO: Exception handler
    db.add(cl)
    db.commit()
    db.refresh(cl)
    return cl


def class_delete(db: Session, class_id: int) -> None:
    cl = db.query(ClassU).filter(ClassU.id == class_id)
    if cl is None:
        raise Exception("Class not found")
    print(cl.count())
    cl.delete()
    db.commit()
