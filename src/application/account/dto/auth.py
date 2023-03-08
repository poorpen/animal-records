from dataclasses import dataclass

from src.application.common.dto.base import DTO


@dataclass
class AuthAccountDTO(DTO):
    email: str
    password: str
