from typing import List

from src.domain.animal.values_objects.animal_visited_location import VisitedLocationID, LocationPointID
from src.domain.animal.values_objects.common import AnimalID
from src.domain.animal.values_objects.animal import \
    Weight, Length, Height, GenderVO, LifeStatusVO, ChipperID, ChippingLocationID
from src.domain.animal.entities.animal_visited_location import AnimalVisitedLocation
from src.domain.animal.entities.animal import Animal
from src.domain.animal.entities.type_of_specific_animal import TypeOfSpecificAnimal

from src.application.animal.dto.animal_visited_location import AnimalVisitedLocationDTO, AnimalVisitedLocationDTOs
from src.application.animal.dto.animal import AnimalDTO, AnimalDTOs
from src.domain.animal_type.value_objects import AnimalTypeID

from src.infrastructure.database.models.animal_visited_location import AnimalVisitedLocationDB
from src.infrastructure.database.models.type_of_specific_animal import TypeOfSpecificAnimalDB
from src.infrastructure.database.models.animal import AnimalDB

from src.infrastructure.mapper.decor import converter


def convert_animal_to_dto(data: AnimalDB | Animal) -> AnimalDTO:
    animal_types_id = [animaL_type.animal_type_id for animaL_type in data.animal_types]
    visited_locations_id = [visited_location.id for visited_location in data.visited_locations]
    return AnimalDTO(
        id=data.id,
        weight=data.weight,
        length=data.length,
        height=data.height,
        animal_types=animal_types_id,
        chipper_id=data.chipper_id,
        chipping_location_id=data.chipping_location_id,
        life_status=data.life_status,
        gender=data.gender,
        chipping_datetime=data.chipping_datetime,
        visited_locations=visited_locations_id,
        death_datetime=data.death_datetime
    )


@converter(AnimalVisitedLocation, AnimalVisitedLocationDTO)
def visited_location_entity_to_dto(data: AnimalVisitedLocation) -> AnimalVisitedLocationDTO:
    return AnimalVisitedLocationDTO(
        id=data.id.to_id(),
        datetime_of_visit=data.datetime_of_visit,
        location_point_id=data.location_point_id.to_id()
    )


@converter(list, AnimalVisitedLocationDTOs)
def visited_location_models_to_dtos_converter(data: List[AnimalVisitedLocationDB]) -> AnimalVisitedLocationDTOs:
    return AnimalVisitedLocationDTOs(
        visited_locations=[
            AnimalVisitedLocationDTO(
                id=model.id,
                datetime_of_visit=model.datetime_of_visit,
                location_point_id=model.location_point_id
            )
            for model in data
        ]
    )


@converter(Animal, AnimalDTO)
def animal_entity_to_dto_converter(data: Animal) -> AnimalDTO:
    visited_locations_id = []
    animal_types_id = [animaL_type.animal_type_id.to_id() for animaL_type in data.animal_types]
    if None not in data.visited_locations:
        visited_locations_id = [visited_location.id.to_id() for visited_location in data.visited_locations]
    return AnimalDTO(
        id=data.id.to_id(),
        weight=data.weight.to_fload(),
        length=data.length.to_fload(),
        height=data.height.to_fload(),
        animal_types=animal_types_id,
        chipper_id=data.chipper_id.to_id(),
        chipping_location_id=data.chipping_location_id.to_id(),
        life_status=data.life_status.to_enum(),
        gender=data.gender.to_enum(),
        chipping_datetime=data.chipping_datetime,
        visited_locations=visited_locations_id,
        death_datetime=data.death_datetime
    )


@converter(Animal, AnimalDB)
def animal_entity_to_model_converter(data: Animal) -> AnimalDB:
    animal_type_models = [
        TypeOfSpecificAnimalDB(animal_type_id=animal_type.animal_type_id.to_id(), animal_id=data.id.to_id())
        for animal_type in data.animal_types]
    visited_location_models = [AnimalVisitedLocationDB(
        id=visited_location.id.to_id(),
        datetime_of_visit=visited_location.datetime_of_visit,
        location_point_id=visited_location.location_point_id.to_id(),
        animal_id=data.id.to_id()
    ) for visited_location in data.visited_locations]
    return AnimalDB(
        id=data.id.to_id(),
        weight=data.weight.to_fload(),
        length=data.length.to_fload(),
        height=data.height.to_fload(),
        animal_types=animal_type_models,
        chipper_id=data.chipper_id.to_id(),
        chipping_location_id=data.chipping_location_id.to_id(),
        life_status=data.life_status.to_enum(),
        gender=data.gender.to_enum(),
        chipping_datetime=data.chipping_datetime,
        visited_locations=visited_location_models,
        death_datetime=data.death_datetime
    )


@converter(AnimalDB, Animal)
def animal_model_to_entity_converter(data: AnimalDB) -> Animal:
    animal_types_entities = [
        TypeOfSpecificAnimal(
            animal_type_id=AnimalTypeID(animal_type.animal_type_id), animal_id=AnimalID(animal_type.animal_id)
        )
        for animal_type in data.animal_types]
    visited_location_entities = [
        AnimalVisitedLocation(
            id=VisitedLocationID(visited_location.id),
            datetime_of_visit=visited_location.datetime_of_visit,
            location_point_id=LocationPointID(visited_location.location_point_id),
            animal_id=AnimalID(visited_location.animal_id)
        )
        for visited_location in data.visited_locations
    ]
    return Animal(
        id=AnimalID(data.id),
        weight=Weight(data.weight),
        length=Length(data.length),
        height=Height(data.height),
        gender=GenderVO(data.gender.value),
        life_status=LifeStatusVO(data.life_status.value),
        chipping_datetime=data.chipping_datetime,
        chipping_location_id=ChippingLocationID(data.chipping_location_id),
        chipper_id=ChipperID(data.chipper_id),
        animal_types=animal_types_entities,
        visited_locations=visited_location_entities,
        death_datetime=data.death_datetime
    )


@converter(AnimalDB, AnimalDTO)
def animal_model_to_dto_converter(data: AnimalDB) -> AnimalDTO:
    return convert_animal_to_dto(data)


@converter(list, AnimalDTOs)
def animal_model_to_dtos_converter(data: List[AnimalDB]) -> AnimalDTOs:
    return AnimalDTOs(animals=[
        convert_animal_to_dto(animal) for animal in data
    ])
