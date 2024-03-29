from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.common.entities.entity import Entity

from src.application.common.interfaces.mapper import IMapper

from src.infrastructure.database.repo.common.exceptions.database_exceptions import LimitError, \
    OffsetError, InvalidID


class SQLAlchemyRepo:

    def __init__(self, session: AsyncSession, mapper: IMapper):
        self._session = session
        self._mapper = mapper

    @staticmethod
    def _validate_limit_offset(limit, offset):
        if limit <= 0:
            raise LimitError()
        elif offset < 0:
            raise OffsetError()

    @staticmethod
    def _validate_id(some_id: int, field: str):
        if some_id <= 0:
            raise InvalidID(field)
