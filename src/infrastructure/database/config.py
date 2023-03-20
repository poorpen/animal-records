from dataclasses import dataclass


@dataclass
class DBConfig:
    host: str
    user: str
    password: str
    db_name: str
    driver: str
    port: int = 5432
