from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class Submission(Base):
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    origin_filename = Column(String)
    status = Column(String)
    result = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))
