from typing import List

from src.domain.animal.entities.animal_visited_location import AnimalVisitedLocation
from src.domain.animal.entities.animal import Animal
from src.domain.animal.entities.type_of_specific_animal import TypeOfSpecificAnimal

from src.application.animal.dto.animal_visited_location import AnimalVisitedLocationDTO, AnimalVisitedLocationDTOs
from src.application.animal.dto.animal import AnimalDTO, AnimalDTOs

from src.infrastructure.database.models.animal_visited_location import AnimalVisitedLocationDB
from src.infrastructure.database.models.type_of_specific_animal import TypeOfSpecificAnimalDB
from src.infrastructure.database.models.animal import AnimalDB

from src.infrastructure.mapper.decor import converter


def convert_to_dto(data: AnimalVisitedLocation | AnimalVisitedLocationDB) -> AnimalVisitedLocationDTO:
    return AnimalVisitedLocationDTO(
        id=data.id,
        datetime_of_visit=data.datetime_of_visit,
        location_point_id=data.location_point_id
    )


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
    return convert_to_dto(data)


@converter(list, AnimalVisitedLocationDTOs)
def visited_location_models_to_dtos_converter(data: List[AnimalVisitedLocationDB]) -> AnimalVisitedLocationDTOs:
    return AnimalVisitedLocationDTOs(
        visited_locations=[
            convert_to_dto(model)
            for model in data
        ]
    )


@converter(Animal, AnimalDTO)
def animal_entity_to_dto_converter(data: Animal) -> AnimalDTO:
    return convert_animal_to_dto(data)


@converter(Animal, AnimalDB)
def animal_entity_to_model_converter(data: Animal) -> AnimalDB:
    animal_type_models = [TypeOfSpecificAnimalDB(animal_type_id=animal_type.animal_type_id, animal_id=data.id)
                          for animal_type in data.animal_types]
    visited_location_models = [AnimalVisitedLocationDB(
        id=visited_location.id,
        datetime_of_visit=visited_location.datetime_of_visit,
        location_point_id=visited_location.location_point_id
    ) for visited_location in data.visited_locations]
    return AnimalDB(
        id=data.id,
        weight=data.weight,
        length=data.length,
        height=data.height,
        gender=data.gender,
        life_status=data.life_status,
        chipping_datetime=data.chipping_datetime,
        chipping_location_id=data.chipping_location_id,
        chipper_id=data.chipper_id,
        death_datetime=data.death_datetime,
        animal_types=animal_type_models,
        visited_locations=visited_location_models
    )


@converter(AnimalDB, Animal)
def animal_model_to_entity_converter(data: AnimalDB) -> Animal:
    animal_types_entities = [
        TypeOfSpecificAnimal(
            animal_id=data.id,
            animal_type_id=animal_type.animal_type_id
        )
        for animal_type in data.animal_types]
    visited_location_entities = [
        AnimalVisitedLocation(
            id=visited_location.id,
            datetime_of_visit=visited_location.datetime_of_visit,
            location_point_id=visited_location.location_point_id
        )
        for visited_location in data.visited_locations
    ]
    return Animal(
        id=data.id,
        weight=data.weight,
        length=data.length,
        height=data.height,
        gender=data.gender,
        life_status=data.life_status,
        chipping_datetime=data.chipping_datetime,
        chipping_location_id=data.chipping_location_id,
        chipper_id=data.chipper_id,
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
