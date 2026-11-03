from collections import Counter
from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Activity, utcnow
from app.schemas.common import SKILLS
from app.schemas.history import DayCount, Stats

SPEAKING_SESSION = timedelta(minutes=30)


def _as_utc(value: datetime) -> datetime:
    return value if value.tzinfo else value.replace(tzinfo=UTC)


async def log(
    db: AsyncSession,
    user_id: int,
    skill: str,
    *,
    score: int | None = None,
    ref_id: int | None = None,
    payload: dict | None = None,
) -> Activity:
    activity = Activity(user_id=user_id, skill=skill, score=score, ref_id=ref_id, payload=payload)
    db.add(activity)
    return activity


async def log_speaking(db: AsyncSession, user_id: int, conversation_id: int, title: str) -> None:
    query = (
        select(Activity.created_at)
        .where(Activity.user_id == user_id, Activity.skill == "speaking", Activity.ref_id == conversation_id)
        .order_by(Activity.created_at.desc())
        .limit(1)
    )
    last = (await db.execute(query)).scalar_one_or_none()
    if last is None or utcnow() - _as_utc(last) > SPEAKING_SESSION:
        await log(db, user_id, "speaking", ref_id=conversation_id, payload={"title": title})


async def recent(db: AsyncSession, user_id: int, limit: int = 30, skill: str | None = None) -> list[Activity]:
    query = select(Activity).where(Activity.user_id == user_id)
    if skill:
        query = query.where(Activity.skill == skill)
    return list((await db.execute(query.order_by(Activity.created_at.desc()).limit(limit))).scalars())


async def stats(db: AsyncSession, user_id: int, tz_offset: int = 0) -> Stats:
    counts = dict(
        (await db.execute(
            select(Activity.skill, func.count()).where(Activity.user_id == user_id).group_by(Activity.skill)
        )).all()
    )
    since = utcnow() - timedelta(days=400)
    rows = (await db.execute(
        select(Activity.created_at).where(Activity.user_id == user_id, Activity.created_at >= since)
    )).scalars()

    offset = timedelta(minutes=tz_offset)
    per_day = Counter((_as_utc(created) + offset).date() for created in rows)
    today = (utcnow() + offset).date()

    cursor = today if today in per_day else today - timedelta(days=1)
    streak = 0
    while cursor in per_day:
        streak += 1
        cursor -= timedelta(days=1)

    days = [
        DayCount(day=(day := today - timedelta(days=27 - i)).isoformat(), count=per_day.get(day, 0))
        for i in range(28)
    ]
    by_skill = {skill: counts.get(skill, 0) for skill in SKILLS}
    return Stats(total=sum(by_skill.values()), streak=streak, by_skill=by_skill, days=days)
