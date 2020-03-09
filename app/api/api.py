from fastapi import APIRouter

from app.api.endpoints import authentication, submissions

router = APIRouter()
router.include_router(authentication.router, prefix="/auth",
                      tags=["authentication"])
router.include_router(submissions.router, prefix="/submit", tags=["submit"])


@router.get("/", description="test path")
async def index():
    return {"detail": "Welcome to OnlineJudge!"}
