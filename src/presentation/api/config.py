from dataclasses import dataclass


@dataclass
class ApiConfig:
    host: str
    port: int