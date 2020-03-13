from pydantic import BaseModel


class SubmissionOut(BaseModel):
    id: int
    origin_filename: str
    user_id: int
    lab_id: int
    code: str
    status: str
    total_score: int = None
    result: str = None
    log: str = None

    class Config:
        orm_mode = True


class SubmissionUpdate(BaseModel):
    id: int
    filename: str
    status: str
    total_score: int
    result: str
    log: str
