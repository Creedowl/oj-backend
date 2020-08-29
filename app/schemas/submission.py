from typing import List, Any

from pydantic import BaseModel
from pydantic.utils import GetterDict


class AddDetail(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if key == "student_id":
            return self._obj.user.student_id
        if key == "lab_name":
            return self._obj.lab.name
        return res


class SubmissionOut(BaseModel):
    id: int
    origin_filename: str
    user_id: int
    student_id: str
    lab_id: int
    lab_name: str
    code: str
    status: str
    total_score: int = None
    result: str = None
    log: str = None

    class Config:
        orm_mode = True
        getter_dict = AddDetail


class SubmissionListOut(BaseModel):
    id: int
    origin_filename: str
    user_id: int
    student_id: str
    lab_id: int
    lab_name: str
    status: str
    total_score: int = None

    class Config:
        orm_mode = True
        getter_dict = AddDetail


class SubmissionsOut(BaseModel):
    total: int
    offset: int
    limit: int
    submissions: List[SubmissionListOut]


class SubmissionUpdate(BaseModel):
    id: int
    filename: str
    status: str
    total_score: int
    result: str
    log: str
