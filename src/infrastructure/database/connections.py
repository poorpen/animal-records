from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.infrastructure.database.config import DBConfig

from src.infrastructure.database.utils.connection_string_maker import make_connection_string


def get_database_connection(config: DBConfig):
    engine = create_async_engine(make_connection_string(config))
    async_sessionmaker = sessionmaker(engine, class_=AsyncSession)
    return async_sessionmaker
