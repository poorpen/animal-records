from dataclasses import dataclass

from src.infrastructure.database.config import DBConfig

from src.presentation.api.config import ApiConfig


@dataclass
class Config:
    database: DBConfig
    api: ApiConfig
