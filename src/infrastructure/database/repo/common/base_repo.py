from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.interfaces.mapper import IMapper


class SQLAlchemyRepo:

    def __init__(self, session: AsyncSession, mapper: IMapper):
        self._session = session
        self._mapper = mapper
