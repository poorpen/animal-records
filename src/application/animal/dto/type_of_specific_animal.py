from src.application.common.dto.base import DTO


class ChangeTypeOfSpecificAnimalDTO(DTO):
    animal_id: int
    old_type_id: int
    new_type_id: int
