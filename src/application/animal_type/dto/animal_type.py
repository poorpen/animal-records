from dataclasses import dataclass

from src.application.common.dto.base import DTO
from src.application.common.dto.id_validator import IDValidator


@dataclass
class TypeID(IDValidator):
    id: int


@dataclass
class BaseAnimalTypeDTO(DTO):
    type: str


class CreateAnimalTypeDTO(BaseAnimalTypeDTO):
    ...


@dataclass
class AnimalTypeDTO(BaseAnimalTypeDTO):
    id: int


class ChangeAnimalTypeDTO(BaseAnimalTypeDTO, TypeID):
    ...
