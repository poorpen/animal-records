from dataclasses import dataclass

from src.application.common.dto.base import DTO
from src.application.animal.dto.common import ValidateAnimalID


@dataclass
class ChangeTypeOfSpecificAnimalDTO(ValidateAnimalID, DTO):
    animal_id: int
    old_type_id: int
    new_type_id: int


@dataclass
class AddTypeOfSpecificAnimalDTO(ValidateAnimalID, DTO):
    animal_id: int
    animal_type_id: int
