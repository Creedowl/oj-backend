from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    student_id: str


class UserCreate(UserBase):
    password: str


class UserDB(UserBase):
    id: int = None

    class Config:
        orm_mode = True


class UserOut(UserBase):
    access_token: str
    token_type: str
