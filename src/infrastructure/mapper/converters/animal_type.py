from src.domain.animal_type.value_objects import AnimalTypeID, AnimalTypeName
from src.domain.animal_type.entities.animal_type import AnimalType

from src.application.animal_type.dto.animal_type import AnimalTypeDTO

from src.infrastructure.database.models.animal_type import AnimalTypeDB

from src.infrastructure.mapper.decor import converter


def convert_to_dto(data: AnimalType) -> AnimalTypeDTO:
    return AnimalTypeDTO(
        id=data.id,
        type=data.type
    )



@converter(AnimalType, AnimalTypeDTO)
def animal_type_entity_to_dto_converter(data: AnimalType) -> AnimalTypeDTO:
    return AnimalTypeDTO(
        id=data.id.to_id(),
        type=data.type.to_string()
    )


@converter(AnimalType, AnimalTypeDB)
def anima_type_entity_to_model_converter(data: AnimalType) -> AnimalTypeDB:
    return AnimalTypeDB(
        id=data.id.to_id(),
        type=data.type.to_string()
    )


@converter(AnimalTypeDB, AnimalType)
def animal_type_model_to_entity_converter(data: AnimalTypeDB) -> AnimalType:
    return AnimalType(
        id=AnimalTypeID(data.id),
        type=AnimalTypeName(data.type)

    )


@converter(AnimalTypeDB, AnimalTypeDTO)
def animal_type_model_to_dto_converter(data: AnimalTypeDB) -> AnimalTypeDTO:
    return convert_to_dto(data)
