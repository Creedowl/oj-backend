from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.utils import config

engine = create_engine(config.DATABASE_URI, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Session:
    try:
        db: Session = SessionLocal()
        yield db
    finally:
        db.close()
