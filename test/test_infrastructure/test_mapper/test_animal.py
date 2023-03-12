import pytest

from datetime import datetime

from src.domain.animal.value_objects.gender import Gender
from src.domain.animal.value_objects.life_status import LifeStatus
from src.domain.animal.entities.animal_visited_location import AnimalVisitedLocation
from src.domain.animal.entities.type_of_specific_animal import TypeOfSpecificAnimal
from src.domain.animal.entities.animal import Animal

from src.application.animal.dto.animal_visited_location import AnimalVisitedLocationDTO, AnimalVisitedLocationDTOs
from src.application.animal.dto.animal import AnimalDTO, AnimalDTOs

from src.infrastructure.database.models.animal_visited_location import AnimalVisitedLocationDB
from src.infrastructure.database.models.type_of_specific_animal import TypeOfSpecificAnimalDB
from src.infrastructure.database.models.animal import AnimalDB

from test.test_infrastructure.test_mapper.common import mapper


@pytest.fixture
def datetime_utcnow():
    return datetime.utcnow()


@pytest.fixture
def animal_visited_location_entity(datetime_utcnow):
    return AnimalVisitedLocation(id=1, location_point_id=1, datetime_of_visit=datetime_utcnow)


@pytest.fixture
def animal_visited_location_dto(datetime_utcnow):
    return AnimalVisitedLocationDTO(id=1, location_point_id=1, datetime_of_visit=datetime_utcnow)


@pytest.fixture
def animal_visited_location_model(datetime_utcnow):
    return AnimalVisitedLocationDB(id=1, location_point_id=1, datetime_of_visit=datetime_utcnow)


@pytest.fixture
def animal_entity(datetime_utcnow):
    return Animal(id=1,
                  weight=1.1,
                  length=1.1,
                  height=1.1,
                  gender=Gender.OTHER,
                  life_status=LifeStatus.ALIVE,
                  chipping_datetime=datetime_utcnow,
                  chipping_location_id=1,
                  chipper_id=1,
                  animal_types=[
                      TypeOfSpecificAnimal(animal_id=1, animal_type_id=2),
                      TypeOfSpecificAnimal(animal_id=1, animal_type_id=1),
                      TypeOfSpecificAnimal(animal_id=1, animal_type_id=3)
                  ],
                  visited_locations=[
                      AnimalVisitedLocation(id=1, datetime_of_visit=datetime_utcnow, location_point_id=1),
                      AnimalVisitedLocation(id=2, datetime_of_visit=datetime_utcnow, location_point_id=2),
                      AnimalVisitedLocation(id=3, datetime_of_visit=datetime_utcnow, location_point_id=3)],
                  death_datetime=None
                  )


@pytest.fixture
def animal_dto(datetime_utcnow):
    return AnimalDTO(id=1,
                     weight=1.1,
                     length=1.1,
                     height=1.1,
                     gender=Gender.OTHER,
                     life_status=LifeStatus.ALIVE,
                     chipping_datetime=datetime_utcnow,
                     chipping_location_id=1,
                     chipper_id=1,
                     animal_types=[2, 1, 3],
                     visited_locations=[1, 2, 3],
                     death_datetime=None)


@pytest.fixture
def animal_model(datetime_utcnow):
    model = AnimalDB(id=1,
                     weight=1.1,
                     length=1.1,
                     height=1.1,
                     gender=Gender.OTHER,
                     life_status=LifeStatus.ALIVE,
                     chipping_datetime=datetime_utcnow,
                     chipping_location_id=1,
                     chipper_id=1,
                     animal_types=[
                         TypeOfSpecificAnimalDB(animal_id=1, animal_type_id=2),
                         TypeOfSpecificAnimalDB(animal_id=1, animal_type_id=1),
                         TypeOfSpecificAnimalDB(animal_id=1, animal_type_id=3)
                     ],
                     visited_locations=[
                         AnimalVisitedLocationDB(id=1, datetime_of_visit=datetime_utcnow, location_point_id=1),
                         AnimalVisitedLocationDB(id=2, datetime_of_visit=datetime_utcnow, location_point_id=2),
                         AnimalVisitedLocationDB(id=3, datetime_of_visit=datetime_utcnow, location_point_id=3)],
                     death_datetime=None)
    for animal_type in model.animal_types:
        animal_type.__dict__.pop('_sa_instance_state')
    for visited_location in model.visited_locations:
        visited_location.__dict__.pop('_sa_instance_state')

    model.__dict__.pop('_sa_instance_state')
    return model


def test_visited_location_entity_to_dto(mapper, animal_visited_location_entity, animal_visited_location_dto):
    result = mapper.load(AnimalVisitedLocationDTO, animal_visited_location_entity)
    assert result == animal_visited_location_dto


def test_visited_location_models_to_dtos(mapper, animal_visited_location_model, animal_visited_location_dto):
    expected_result = AnimalVisitedLocationDTOs(
        visited_locations=[animal_visited_location_dto, animal_visited_location_dto, animal_visited_location_dto])
    result = mapper.load(AnimalVisitedLocationDTOs,
                         [animal_visited_location_model, animal_visited_location_model, animal_visited_location_model])
    assert result == expected_result


def test_animal_entity_to_dto(mapper, animal_entity, animal_dto):
    result = mapper.load(AnimalDTO, animal_entity)
    assert result == animal_dto


def test_animal_entity_to_model(mapper, animal_entity, animal_model):
    result = mapper.load(AnimalDB, animal_entity)

    for animal_type, exp_animal_type in zip(result.animal_types, animal_model.animal_types):
        animal_type.__dict__.pop('_sa_instance_state')
        assert animal_type.__dict__ == exp_animal_type.__dict__
        assert type(animal_type) == type(exp_animal_type)

    for visited_location, exp_visited_location in zip(result.visited_locations, animal_model.visited_locations):
        visited_location.__dict__.pop('_sa_instance_state')
        assert visited_location.__dict__ == exp_visited_location.__dict__
        assert type(visited_location) == type(exp_visited_location)

    animal_model.__dict__.pop('animal_types')
    animal_model.__dict__.pop('visited_locations')

    result.__dict__.pop('_sa_instance_state')
    result.__dict__.pop('animal_types')
    result.__dict__.pop('visited_locations')

    assert result.__dict__ == animal_model.__dict__
    assert type(result) == type(animal_model)



def test_animal_model_to_entity(mapper, animal_model, animal_entity):
    result = mapper.load(Animal, animal_model)
    assert result == animal_entity


def test_animal_model_to_dto(mapper, animal_model, animal_dto):
    result = mapper.load(AnimalDTO, animal_model)
    assert result == animal_dto


def test_animal_model_to_dtos(mapper, animal_model, animal_dto):
    expected_result = AnimalDTOs(animals=[animal_dto, animal_dto, animal_dto])
    result = mapper.load(AnimalDTOs, [animal_model, animal_model, animal_model])
    assert result == expected_result
