from src.application.animal_type.dto.animal_type import AnimalTypeDTO

from src.infrastructure.mapper.decor import converter

from src.presentation.api.handlers.animal_type.responses.animal_type import AnimalTypeVM


@converter(AnimalTypeDTO, AnimalTypeVM)
def convert_animal_type_dto_to_vm(data: AnimalTypeDTO) -> AnimalTypeVM:
    return AnimalTypeVM(
        id=data.id,
        type=data.type,
        by_alies=True
    )
