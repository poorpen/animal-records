from src.domain.animal_type.entities.animal_type import AnimalType

from src.application.animal_type.dto.animal_type import AnimalTypeDTO

from src.infrastructure.database.models.animal_type import AnimalTypeDB


def animal_type_entity_to_dto(data: AnimalType) -> AnimalTypeDTO:
    return AnimalTypeDTO(
        id=data.id,
        type=data.type
    )


def anima_type_entity_to(data: AnimalType) -> AnimalTypeDB:
    return AnimalTypeDB(
        id=data.id,
        type=data.type
    )


def animal_type_model_to_entity(data: AnimalTypeDB) -> AnimalType:
    return AnimalType(
        id=data.id,
        type=data.type

    )


def animal_type_model_to_dto(data: AnimalTypeDB) -> AnimalTypeDTO:
    return AnimalTypeDTO(
        id=data.id,
        type=data.type
    )
