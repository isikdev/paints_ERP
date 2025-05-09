from typing import Union
from uuid import UUID

from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User

class UserDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_user_by_id(self, user_id: UUID) -> Union[User, None]:
        query = select(User).where(User.id == user_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def get_user_by_email(self, email: str) -> Union[User, None]:
        query = select(User).where(User.email == email)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def update_user(self, user_id: UUID, **kwargs) -> Union[UUID, None]:
        query = (
            update(User)
            .where(and_(User.id == user_id, User.is_active == True))
            .values(kwargs)
            .returning(User)
        )
        res = await self.db_session.execute(query)
        update_user = res.fetchone()
        if update_user is not None:
            return update_user[0]
