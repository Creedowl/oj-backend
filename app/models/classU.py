from sqlalchemy import Column, Integer, String

from app.models.base import Base


class ClassU(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    teacher = Column(String)
