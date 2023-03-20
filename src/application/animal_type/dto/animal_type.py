from dataclasses import dataclass

from src.application.common.dto.base import DTO


@dataclass
class BaseAnimalTypeDTO(DTO):
    type: str


class CreateAnimalTypeDTO(BaseAnimalTypeDTO):
    ...


@dataclass
class AnimalTypeDTO(BaseAnimalTypeDTO):
    id: int


@dataclass
class ChangeAnimalTypeDTO(BaseAnimalTypeDTO):
    id: int
