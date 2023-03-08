from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.interfaces.mapper import IMapper

from src.infrastructure.database.repo.common.interfaces.error_parser import IErrorParser
from src.infrastructure.database.repo.common.base_query_bilder import BaseQueryBuilder


class SQLAlchemyRepo:

    def __init__(self, session: AsyncSession, mapper: IMapper, error_parser: IErrorParser,
                 query_builder: BaseQueryBuilder = None):
        self._session = session
        self._mapper = mapper
        self._error_parser = error_parser
        self._query_builder = query_builder
