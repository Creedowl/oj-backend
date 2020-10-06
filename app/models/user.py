from sqlalchemy import Column, Integer, String, Boolean

from app.models.base import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    student_id = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean)
