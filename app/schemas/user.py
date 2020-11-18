from pydantic import BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from app.models.user import User
# sqlalchemy use this to find ClassU
from app.models.classU import ClassU

UserInfo = sqlalchemy_to_pydantic(User, exclude=["hashed_password"])


class UserBase(BaseModel):
    name: str
    student_id: str


class UserCreate(UserBase):
    password: str


# class UserUpdate(UserBase):
#     id: int
#     password: str
#     classU_id: int

class UserUpdate(BaseModel):
    old_password: str = None
    new_password: str = None
    classU_id: int = None


class UserDB(UserBase):
    is_admin: bool
    classU_id: int
    id: int = None

    class Config:
        orm_mode = True


class UserOut(UserInfo):
    access_token: str
    token_type: str
