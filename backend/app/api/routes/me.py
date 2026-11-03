from fastapi import APIRouter

from app.api.deps import CurrentUser
from app.schemas.history import Profile

router = APIRouter(tags=["profile"])


@router.get("/me", response_model=Profile)
async def me(user: CurrentUser) -> Profile:
    return Profile(name=user.name, created_at=user.created_at)
