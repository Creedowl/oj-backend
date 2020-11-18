from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    student_id = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean)
    classU_id = Column(Integer, ForeignKey("classu.id", ondelete='SET NULL'))
    classU = relationship("ClassU", backref="students")
