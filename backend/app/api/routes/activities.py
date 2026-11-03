from fastapi import APIRouter, Query

from app.api.deps import CurrentUser, Db
from app.repositories import activities
from app.schemas.history import ActivityIn, ActivityOut, Stats

router = APIRouter(tags=["progress"])


def _out(activity) -> ActivityOut:
    return ActivityOut(
        id=activity.id,
        skill=activity.skill,
        score=activity.score,
        payload=activity.payload,
        created_at=activity.created_at,
    )


@router.get("/activities", response_model=list[ActivityOut])
async def list_activities(db: Db, user: CurrentUser, limit: int = Query(30, ge=1, le=200)) -> list[ActivityOut]:
    return [_out(a) for a in await activities.recent(db, user.id, limit)]


@router.post("/activities", response_model=ActivityOut, status_code=201)
async def create_activity(body: ActivityIn, db: Db, user: CurrentUser) -> ActivityOut:
    activity = await activities.log(db, user.id, body.skill, score=body.score, payload=body.payload)
    await db.commit()
    return _out(activity)


@router.get("/stats", response_model=Stats)
async def get_stats(db: Db, user: CurrentUser, tz_offset: int = Query(0, ge=-840, le=840)) -> Stats:
    return await activities.stats(db, user.id, tz_offset)
