from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.interfaces.uow.base import IUoW


class BaseUoW(IUoW):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
