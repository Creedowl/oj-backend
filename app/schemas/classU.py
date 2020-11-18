from typing import List

from pydantic import BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from app.models.classU import ClassU
from app.schemas.user import UserInfo

ClassUBase = sqlalchemy_to_pydantic(ClassU)


# class ClassUBase(BaseModel):
#     name: str
#     teacher: str


class ClassUInfo(ClassUBase):
    students: List[UserInfo] = []


# class ClassUIn(ClassUBase):
#     pass

ClassCreate = sqlalchemy_to_pydantic(ClassU, exclude=['id'])


class ClassUDB(ClassUBase):
    id: int

    class Config:
        orm_mode = True


class ClassUOut(ClassUDB):
    pass


class ClassDelete(BaseModel):
    result: bool
