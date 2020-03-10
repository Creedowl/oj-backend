from pydantic import BaseModel


class LabBase(BaseModel):
    name: str
    title: str
    content: str


class LabIn(LabBase):
    pass


class LabDB(LabBase):
    id: int

    class Config:
        orm_mode = True


class LabOut(LabDB):
    pass
