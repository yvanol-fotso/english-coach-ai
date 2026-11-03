from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User


async def _find(db: AsyncSession, key: str) -> User | None:
    return (await db.execute(select(User).where(User.key == key))).scalar_one_or_none()


async def get_or_create(db: AsyncSession, name: str) -> User:
    key = name.casefold()
    user = await _find(db, key)
    if user is None:
        user = User(key=key, name=name)
        db.add(user)
        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            user = await _find(db, key)
    await db.commit()
    return user
