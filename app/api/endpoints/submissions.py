import os
import uuid

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.lab import lab_get
from app.db.submission import submission_create, submission_get_list, submission_update, submission_get, \
    submission_export
from app.models.user import User
from app.schemas.submission import SubmissionOut, SubmissionUpdate, SubmissionsOut
from app.utils import config
from app.utils.excel import export_excel
from app.utils.security import get_current_user

router = APIRouter()


@router.get("/", response_model=SubmissionsOut)
def get_submissions(
        db: Session = Depends(get_db),
        offset: int = 0,
        limit: int = 100,
        lab_id: int = None,
        user_id: int = None
):
    """
    get submissions according to the given filter
    """
    submissions = submission_get_list(db, offset, limit, lab_id, user_id)
    return {
        "total": submissions["count"],
        "limit": limit,
        "offset": offset,
        "submissions": submissions["submissions"]
    }


@router.get("/{submission_id}", response_model=SubmissionOut)
def get_submission(
        *,
        db: Session = Depends(get_db),
        submission_id: int,
        user: User = Depends(get_current_user),
):
    submission = submission_get(db, submission_id)
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Submission '{submission_id}' not found"
        )
    if submission.user_id != user.id and not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission deny"
        )
    if not user.is_admin:
        submission.log = ""
    return {
        **submission.__dict__,
        "student_id": submission.user.student_id,
        "lab_name": submission.lab.name
    }


@router.post("/submit/{lab_id}/", response_model=SubmissionOut)
def submit(
        *,
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user),
        lab_id: int
):
    """
    submit file to the server
    """
    if file.filename.split('.')[-1] not in config.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Disallowed file type"
        )
    if not lab_get(db, lab_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Lab '{lab_id}' doesn't exist"
        )
    content = file.file.read()
    filename = str(uuid.uuid4())
    with open(os.path.join(config.UPLOAD_FOLDER, filename), "wb") as f:
        f.write(content)
    file.file.close()
    res = submission_create(db, {
        "filename": filename,
        "origin_filename": file.filename,
        "code": str(content, encoding="utf-8"),
        "total_score": 0,
        "status": "pending",
        "user_id": user.id,
        "lab_id": lab_id
    })
    return res


@router.post("/update", response_model=SubmissionOut)
def oj_callback(
        *,
        db: Session = Depends(get_db),
        update: SubmissionUpdate
):
    # use the uuid filename as a secret, so never send the uuid filename to user
    submission = submission_get(db, update.id, update.filename)
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No such submission found"
        )
    return submission_update(db, submission, update)


@router.get("/export/{class_id}", response_description='xlsx')
def export(
        *,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user),
        class_id: int
):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission deny"
        )
    headers = {
        'Content-Disposition': 'attachment; filename="export.xlsx"'
    }
    submissions = submission_export(db, class_id)
    output = export_excel(submissions)
    return StreamingResponse(output, headers=headers)
