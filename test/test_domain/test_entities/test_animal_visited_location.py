import pytest

from unittest import mock

from datetime import datetime

from src.domain.animal.services.anima_visited_locations import add_visited_location, change_visited_location, \
    delete_visited_location

from src.domain.animal.exceptions.animal_visited_location import LocationPointEqualToChippingLocation, \
    AnimalNowInThisPoint, UpdateToSameLocationPoint, NextOfPreviousEqualThisLocation, AnimalHasNoCurrentVisitedLocation, \
    UpdatedFirstPointToChippingPoint
from src.domain.animal.exceptions.animal import AnimalIsDead

from src.domain.animal.value_objects.life_status import LifeStatus
from src.domain.animal.entities.animal_visited_location import AnimalVisitedLocation
from src.domain.common.exceptions.validation import IntegerMin

from test.test_domain.test_entities.common import animal


@pytest.fixture()
def visited_location():
    return AnimalVisitedLocation(id=1, location_point_id=4, datetime_of_visit=datetime.utcnow())


def test_add_visited_location_negative_first(animal, visited_location):
    animal.life_status = LifeStatus.DEAD
    with pytest.raises(AnimalIsDead):
        add_visited_location(animal, visited_location.location_point_id)


def test_add_visited_location_negative_second(animal, visited_location):
    visited_location.location_point_id = animal.chipping_location_id
    with pytest.raises(LocationPointEqualToChippingLocation):
        add_visited_location(animal, visited_location.location_point_id)


def test_add_visited_location_negative_third(animal, visited_location):
    animal.visited_locations.append(visited_location)
    with pytest.raises(AnimalNowInThisPoint):
        add_visited_location(animal, visited_location.location_point_id)


def test_add_visited_location_negative_fourth(animal):
    with pytest.raises(IntegerMin):
        add_visited_location(animal, 0)


@mock.patch('src.domain.animal.services.anima_visited_locations.datetime')
def test_add_visited_location_positive(mock_datetime, animal):
    location_point_id = 6
    returned_datetime = datetime.utcnow()
    mock_datetime.utcnow = mock.Mock(return_value=returned_datetime)
    add_visited_location(animal, location_point_id)
    expected_visited_location = AnimalVisitedLocation(id=None, location_point_id=location_point_id,
                                                      datetime_of_visit=returned_datetime)
    assert expected_visited_location in animal.visited_locations


def test_change_visited_location_negative_first(animal, visited_location):
    with pytest.raises(AnimalHasNoCurrentVisitedLocation):
        change_visited_location(animal, visited_location.id, visited_location.location_point_id)


def test_change_visited_location_negative_second(animal, visited_location):
    animal.visited_locations.append(visited_location)
    with pytest.raises(UpdateToSameLocationPoint):
        change_visited_location(animal, visited_location.id, visited_location.location_point_id)


def test_change_visited_location_negative_third(animal, visited_location):
    location_point_id = visited_location.location_point_id + 2
    visited_location_id = visited_location.id + 5
    animal.update(visited_locations=[
        visited_location,
        AnimalVisitedLocation(id=visited_location_id, datetime_of_visit=datetime.utcnow(),
                              location_point_id=location_point_id),
        AnimalVisitedLocation(id=visited_location_id + 2,
                              datetime_of_visit=datetime.utcnow(),
                              location_point_id=visited_location.location_point_id + 10)])
    with pytest.raises(NextOfPreviousEqualThisLocation):
        change_visited_location(animal, visited_location_id, visited_location.location_point_id)


def test_change_visited_location_negative_fourth(animal, visited_location):
    location_point_id = visited_location.location_point_id + 2
    visited_location_id = visited_location.id + 5
    animal.update(visited_locations=[
        AnimalVisitedLocation(id=visited_location_id + 2,
                              datetime_of_visit=datetime.utcnow(),
                              location_point_id=visited_location.location_point_id + 10),
        AnimalVisitedLocation(id=visited_location_id,
                              datetime_of_visit=datetime.utcnow(),
                              location_point_id=location_point_id),
        visited_location,
    ])
    with pytest.raises(NextOfPreviousEqualThisLocation):
        change_visited_location(animal, visited_location_id, visited_location.location_point_id)


def test_change_visited_location_negative_fifth(animal, visited_location):
    visited_location.location_point_id += 2
    animal.update(visited_locations=[visited_location])
    with pytest.raises(UpdatedFirstPointToChippingPoint):
        change_visited_location(animal, visited_location.id, animal.chipping_location_id)


def test_change_visited_location_negative_sixth(animal):
    with pytest.raises(IntegerMin):
        change_visited_location(animal, 0, 1)


def test_change_visited_location_negative_seventh(animal, visited_location):
    animal.visited_locations.append(visited_location)
    with pytest.raises(IntegerMin):
        change_visited_location(animal, 1, 0)


def test_change_visited_location_positive(animal, visited_location):
    new_location_id = 69
    animal.update(visited_locations=[visited_location])
    change_visited_location(animal, visited_location.id, new_location_id)
    visited_location = animal.get_visited_location(visited_location.id)
    assert visited_location == AnimalVisitedLocation(id=visited_location.id, location_point_id=new_location_id,
                                                     datetime_of_visit=visited_location.datetime_of_visit)


def test_delete_visited_location_negative(animal, visited_location):
    with pytest.raises(AnimalHasNoCurrentVisitedLocation):
        delete_visited_location(animal, visited_location.id)


def test_delete_visited_location_positive_first(animal, visited_location):
    animal.update(visited_locations=[visited_location])
    delete_visited_location(animal, visited_location.id)
    assert visited_location not in animal.visited_locations


def test_delete_visited_location_positive_second(animal, visited_location):
    next_visited_location = AnimalVisitedLocation(id=visited_location.id + 5,
                                                  location_point_id=animal.chipping_location_id,
                                                  datetime_of_visit=datetime.utcnow())
    animal.update(
        visited_locations=[visited_location, next_visited_location],
    )
    delete_visited_location(animal, visited_location.id)
    assert visited_location not in animal.visited_locations and next_visited_location not in animal.visited_locations
