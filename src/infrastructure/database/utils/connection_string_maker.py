from src.infrastructure.database.config import DBConfig


def make_connection_string(db_config: DBConfig):
    return (
        f"{db_config.driver}://{db_config.user}:{db_config.password}@{db_config.host}:{db_config.port}/{db_config.db_name}"
    )
