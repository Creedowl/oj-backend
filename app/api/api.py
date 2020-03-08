from fastapi import APIRouter, Depends

from app.api.endpoints import authentication

router = APIRouter()
router.include_router(authentication.router, prefix="/auth",
                      tags=["authentication"])


@router.get("/", description="test path")
async def index():
    return {"detail": "Welcome to OnlineJudge!"}
