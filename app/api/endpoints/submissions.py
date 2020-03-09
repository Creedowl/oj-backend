import os
import uuid
from typing import List

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.submission import submission_create, submission_get_all
from app.models.user import User
from app.schemas.submission import SubmissionOut
from app.utils import config
from app.utils.security import get_current_user

router = APIRouter()


@router.get("/", response_model=List[SubmissionOut])
def get_all_submission(
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user),
        offset: int = 0,
        limit: int = 100
):
    """
    get user's all submissions
    """
    return submission_get_all(db, user.id, offset, limit)


@router.post("/", response_model=SubmissionOut)
def submit(
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    """
    submit file to server
    """
    if file.filename.split('.')[-1] not in config.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Disallowed file type"
        )
    content = file.file.read()
    filename = str(uuid.uuid4())
    with open(os.path.join(config.UPLOAD_FOLDER, filename), "wb") as f:
        f.write(content)
    file.file.close()
    res = submission_create(db, {
        "filename": filename,
        "origin_filename": file.filename,
        "status": "pending",
        "user_id": user.id
    })
    return res
