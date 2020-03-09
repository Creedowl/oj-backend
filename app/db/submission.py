from typing import List

from sqlalchemy.orm import Session

from app.models.submission import Submission


def submission_create(db: Session, data: dict) -> Submission:
    save = Submission(**data)
    db.add(save)
    db.commit()
    db.refresh(save)
    return save


def submission_get_all(
        db: Session, user_id: int, offset: int = 0, limit: int = 100
) -> List[Submission]:
    return db.query(Submission).filter(Submission.user_id == user_id) \
        .offset(offset).limit(limit).all()
