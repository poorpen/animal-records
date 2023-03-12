import pytest

from src.domain.location_point.entities.location_point import LocationPoint

from src.application.location_point.dto.location_point import LocationPointDTO

from src.infrastructure.database.models.location_point import LocationPointDB

from test.test_infrastructure.test_mapper.common import mapper


@pytest.fixture
def location_point_entity():
    return LocationPoint(id=1, latitude=1.1, longitude=1.1)


@pytest.fixture
def location_point_dto():
    return LocationPointDTO(id=1, latitude=1.1, longitude=1.1)


@pytest.fixture
def location_point_model():
    model = LocationPointDB(id=1, latitude=1.1, longitude=1.1)
    model.__dict__.pop('_sa_instance_state')
    return model


def test_entity_to_dto(mapper, location_point_entity, location_point_dto):
    result = mapper.load(LocationPointDTO, location_point_entity)
    assert result == location_point_dto


def test_entity_to_model(mapper, location_point_entity, location_point_model):
    result = mapper.load(LocationPointDB, location_point_entity)
    result.__dict__.pop('_sa_instance_state')
    assert result.__dict__ == location_point_model.__dict__
    assert type(result) == type(location_point_model)


def test_model_to_entity(mapper, location_point_model, location_point_entity):
    result = mapper.load(LocationPoint, location_point_model)
    assert result == location_point_entity


def test_model_to_dto(mapper, location_point_model, location_point_dto):
    result = mapper.load(LocationPointDTO, location_point_model)
    assert result == location_point_dto



