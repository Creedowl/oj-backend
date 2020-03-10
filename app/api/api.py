from fastapi import APIRouter

from app.api.endpoints import authentication, submissions, users

router = APIRouter()
router.include_router(authentication.router, prefix="/auth",
                      tags=["authentication"])
router.include_router(submissions.router, prefix="/submit", tags=["submit"])
router.include_router(users.router, prefix="/users", tags=["users"])


@router.get("/", description="test path")
async def index():
    return {"detail": "Welcome to OnlineJudge!"}
