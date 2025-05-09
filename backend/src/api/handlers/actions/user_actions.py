from typing import Union
from uuid import UUID

from db.dals import UserDAL
from db.models import User

class UserActions:
    """Class containing actions for user, i.e. logic of session context managers and DAL calls."""
    DAL = UserDAL

    @classmethod
    async def update_user(
        cls, updated_user_params: dict, user_id: UUID, session
    ) -> Union[UUID, None]:
        async with session.begin():
            user_dal = cls.DAL(session)
            updated_user_id = await user_dal.update_user(
                user_id=user_id, **updated_user_params
            )
            return updated_user_id

    @classmethod
    async def get_user_by_id(cls, user_id, session) -> Union[User, None]:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.get_user_by_id(
                user_id=user_id,
            )
            if user is not None:
                return user
