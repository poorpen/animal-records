from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.mapper.mapper import Mapper
from src.infrastructure.mapper.main import build_mapper
from src.infrastructure.database.connections import get_database_connection
from src.infrastructure.database.uow.uow import UoW
from src.infrastructure.database.uow.main import build_uow

from src.presentation.config.config import Config
from src.presentation.api.presenter.main import build_presenter
from src.presentation.api.presenter.presenter import Presenter
from src.presentation.api.providers.abstract.common import session_provider, mapper_provider


def database_session(config: Config):
    sessionmaker = get_database_connection(config.database)

    async def get_database_session() -> AsyncSession:
        async with sessionmaker() as session:
            yield session

    return get_database_session


def mapper_getter() -> Mapper:
    mapper = build_mapper()
    return mapper


def presenter_getter() -> Presenter:
    presenter = build_presenter()
    return presenter


def uow_getter(session: AsyncSession = Depends(session_provider),
               mapper: Mapper = Depends(mapper_provider)) -> UoW:
    return build_uow(
        session=session,
        mapper=mapper
    )
