from dataclasses import dataclass

from src.application.common.dto.base import DTO
from src.application.common.dto.id_validator import IDValidator


@dataclass
class LocationPointID(IDValidator):
    id: int


@dataclass
class BaseLocationPointDTO(DTO):
    latitude: float
    longitude: float


class CreateLocationPointDTO(BaseLocationPointDTO):
    ...


class ChangeLocationPointDTO(BaseLocationPointDTO, LocationPointID):
    ...


@dataclass
class LocationPointDTO(BaseLocationPointDTO):
    id: int
