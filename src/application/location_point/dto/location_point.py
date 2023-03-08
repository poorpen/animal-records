from dataclasses import dataclass

from src.application.common.dto.base import DTO


@dataclass
class BaseLocationPointDTO(DTO):
    latitude: float
    longitude: float


class CreateLocationPointDTO(BaseLocationPointDTO):
    ...


class LocationPointDTO(BaseLocationPointDTO):
    id: int


class ChangeLocationPointDTO(BaseLocationPointDTO):
    id: int
