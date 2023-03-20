import pytest

from src.domain.animal_type.value_objects import AnimalTypeID, AnimalTypeName
from src.domain.animal_type.entities.animal_type import AnimalType

from src.application.animal_type.dto.animal_type import AnimalTypeDTO

from src.infrastructure.database.models.animal_type import AnimalTypeDB

from test.test_infrastructure.test_mapper.common import mapper


@pytest.fixture
def animal_type_entity():
    return AnimalType(id=AnimalTypeID(1), type=AnimalTypeName('some_type'))


@pytest.fixture
def animal_type_dto():
    return AnimalTypeDTO(id=1, type='some_type')


@pytest.fixture
def animal_type_model():
    model = AnimalTypeDB(id=1, type='some_type')
    model.__dict__.pop('_sa_instance_state')
    return model


def test_entity_to_dto(mapper, animal_type_entity, animal_type_dto):
    result = mapper.load(AnimalTypeDTO, animal_type_entity)
    assert result == animal_type_dto


def test_entity_to_model(mapper, animal_type_entity, animal_type_model):
    result = mapper.load(AnimalTypeDB, animal_type_entity)
    result.__dict__.pop('_sa_instance_state')
    assert result.__dict__ == animal_type_model.__dict__
    assert type(result) == type(animal_type_model)


def test_model_to_entity(mapper, animal_type_model, animal_type_entity):
    result = mapper.load(AnimalType, animal_type_model)
    assert result == animal_type_entity


def test_model_to_dto(mapper, animal_type_model, animal_type_dto):
    result = mapper.load(AnimalTypeDTO, animal_type_model)
    assert result == animal_type_dto
