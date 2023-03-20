from dataclasses import dataclass

from src.application.common.dto.base import DTO


@dataclass
class ChangeTypeOfSpecificAnimalDTO(DTO):
    animal_id: int
    old_type_id: int
    new_type_id: int


@dataclass
class AddTypeOfSpecificAnimalDTO(DTO):
    animal_id: int
    animal_type_id: int
