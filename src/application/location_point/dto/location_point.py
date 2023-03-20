from dataclasses import dataclass

from src.application.common.dto.base import DTO


@dataclass
class BaseLocationPointDTO(DTO):
    latitude: float
    longitude: float


class CreateLocationPointDTO(BaseLocationPointDTO):
    ...


@dataclass
class ChangeLocationPointDTO(BaseLocationPointDTO):
    id: int


@dataclass
class LocationPointDTO(BaseLocationPointDTO):
    id: int
