from fastapi import APIRouter

from app.api.endpoints import authentication, submissions, users, labs

router = APIRouter()
router.include_router(authentication.router, prefix="/auth",
                      tags=["authentication"])
router.include_router(submissions.router, prefix="/submissions", tags=["submit"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(labs.router, prefix="/labs", tags=["labs"])


@router.get("/", description="test path")
async def index():
    return {"detail": "Welcome to OnlineJudge!"}
