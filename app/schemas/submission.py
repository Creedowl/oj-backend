from pydantic import BaseModel


class SubmissionOut(BaseModel):
    id: int
    origin_filename: str
    user_id: int
    status: str
    result: str = None

    class Config:
        orm_mode = True
