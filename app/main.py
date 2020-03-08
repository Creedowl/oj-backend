import uvicorn
from fastapi import FastAPI

from app.api import api
from app.db.database import engine
from app.models.base import Base
from app.utils import config

# create database tables
Base.metadata.create_all(engine)

app = FastAPI(title=config.TITLE, version=config.VERSION)

app.include_router(api.router, prefix="/api")

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
