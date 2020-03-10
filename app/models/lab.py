from sqlalchemy import Column, Integer, String

from app.models.base import Base


class Lab(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    title = Column(String)
    content = Column(String)
