from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.submission import Submission
from app.schemas.submission import SubmissionUpdate


def submission_create(db: Session, data: dict) -> Submission:
    save = Submission(**data)
    db.add(save)
    db.commit()
    db.refresh(save)
    return save


def submission_get(db: Session, submission_id: int, filename: str = None) \
        -> Optional[Submission]:
    fil = [Submission.id == submission_id]
    # filename is an optional filter, used by judge server for updating
    if filename is not None:
        fil.append(Submission.filename == filename)
    return db.query(Submission).filter(*fil).first()


def submission_get_list(
        db: Session,
        offset: int = 0,
        limit: int = 100,
        lab_id: int = None,
        user_id: int = None
) -> List[Submission]:
    fil = []
    if lab_id is not None:
        fil.append(Submission.lab_id == lab_id)
    if user_id is not None:
        fil.append(Submission.user_id == user_id)
    return db.query(Submission).filter(*fil).offset(offset).limit(limit).all()


def submission_update(
        db: Session,
        submission: Submission,
        update: SubmissionUpdate
) -> Submission:
    submission.status = update.status
    submission.result = update.result
    submission.total_score = update.total_score
    submission.log = update.log
    db.commit()
    db.refresh(submission)
    return submission
