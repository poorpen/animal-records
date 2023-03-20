from environs import Env

from src.infrastructure.database.config import DBConfig
from src.presentation.api.config import ApiConfig
from src.presentation.config.config import Config


def config_loader():
    env = Env()
    env.read_env()
    return Config(
        api=ApiConfig(host=env.str("API_HOST"),
                      port=env.int("API_PORT")),
        database=DBConfig(host=env.str("DB_HOST"),
                          db_name=env.str("DB_NAME"),
                          password=env.str("DB_PASS"),
                          user=env.str("DB_USER"),
                          driver=env.str("DB_DRIVER"))
    )
