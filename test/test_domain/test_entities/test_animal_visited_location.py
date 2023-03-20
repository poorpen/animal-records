import pytest

from unittest import mock

from datetime import datetime
from src.domain.animal.values_objects.common import AnimalID
from src.domain.animal.services.anima_visited_locations import add_visited_location, change_visited_location, \
    delete_visited_location

from src.domain.animal.exceptions.animal_visited_location import LocationPointEqualToChippingLocation, \
    AnimalNowInThisPoint, UpdateToSameLocationPoint, NextOfPreviousEqualThisLocation, AnimalHasNoCurrentVisitedLocation, \
    UpdatedFirstPointToChippingPoint
from src.domain.animal.exceptions.animal import AnimalIsDead

from src.domain.animal.entities.animal_visited_location import AnimalVisitedLocation
from src.domain.animal.values_objects.animal_visited_location import VisitedLocationID, LocationPointID
from src.domain.common.exceptions.validation import IntegerMin, InvalidID

from test.test_domain.test_entities.common import animal


@pytest.fixture()
def visited_location():
    return AnimalVisitedLocation(id=VisitedLocationID(1), location_point_id=LocationPointID(4),
                                 datetime_of_visit=datetime.utcnow(), animal_id=AnimalID(1))


def test_add_visited_location_negative_first(animal, visited_location):
    animal.life_status.value = "DEAD"
    with pytest.raises(AnimalIsDead):
        add_visited_location(animal, visited_location.location_point_id.to_id())


def test_add_visited_location_negative_second(animal, visited_location):
    animal.chipping_location_id.value = visited_location.location_point_id.value
    visited_location.location_point_id = animal.chipping_location_id
    with pytest.raises(LocationPointEqualToChippingLocation):
        add_visited_location(animal, visited_location.location_point_id.to_id())


def test_add_visited_location_negative_third(animal, visited_location):
    animal.visited_locations.append(visited_location)
    with pytest.raises(AnimalNowInThisPoint):
        add_visited_location(animal, visited_location.location_point_id.to_id())


def test_add_visited_location_negative_fourth(animal):
    with pytest.raises(InvalidID):
        add_visited_location(animal, 0)


@mock.patch('src.domain.animal.services.anima_visited_locations.datetime')
def test_add_visited_location_positive(mock_datetime, animal):
    location_point_id = 6
    returned_datetime = datetime.utcnow()
    mock_datetime.utcnow = mock.Mock(return_value=returned_datetime)
    add_visited_location(animal, location_point_id)
    expected_visited_location = AnimalVisitedLocation(id=VisitedLocationID(None), location_point_id=LocationPointID(location_point_id),
                                                      datetime_of_visit=returned_datetime, animal_id=animal.id)
    assert expected_visited_location in animal.visited_locations


def test_change_visited_location_negative_first(animal, visited_location):
    with pytest.raises(AnimalHasNoCurrentVisitedLocation):
        change_visited_location(animal, visited_location.id.to_id(), visited_location.location_point_id.to_id())


def test_change_visited_location_negative_second(animal, visited_location):
    animal.visited_locations.append(visited_location)
    with pytest.raises(UpdateToSameLocationPoint):
        change_visited_location(animal, visited_location.id.to_id(), visited_location.location_point_id.to_id())


def test_change_visited_location_negative_third(animal, visited_location):
    location_point_id = visited_location.location_point_id.value + 2
    visited_location_id = visited_location.id.value + 5
    animal.update(visited_locations=[
        visited_location,
        AnimalVisitedLocation(id=VisitedLocationID(visited_location_id), datetime_of_visit=datetime.utcnow(),
                              location_point_id=LocationPointID(location_point_id), animal_id=animal.id),
        AnimalVisitedLocation(id=VisitedLocationID(visited_location_id + 2),
                              datetime_of_visit=datetime.utcnow(),
                              location_point_id=LocationPointID(visited_location.location_point_id.value + 10),
                              animal_id=animal.id)])
    with pytest.raises(NextOfPreviousEqualThisLocation):
        change_visited_location(animal, visited_location_id, visited_location.location_point_id.to_id())


def test_change_visited_location_negative_fourth(animal, visited_location):
    location_point_id = visited_location.location_point_id.value + 2
    visited_location_id = visited_location.id.value + 5
    animal.update(visited_locations=[
        AnimalVisitedLocation(id=VisitedLocationID(visited_location_id + 2),
                              datetime_of_visit=datetime.utcnow(),
                              location_point_id=LocationPointID(visited_location.location_point_id.value + 10),
                              animal_id=animal.id),
        AnimalVisitedLocation(id=VisitedLocationID(visited_location_id), datetime_of_visit=datetime.utcnow(),
                              location_point_id=LocationPointID(location_point_id), animal_id=animal.id),
        visited_location,
    ])
    with pytest.raises(NextOfPreviousEqualThisLocation):
        change_visited_location(animal, visited_location_id, visited_location.location_point_id.to_id())


def test_change_visited_location_negative_fifth(animal, visited_location):
    visited_location.location_point_id.value += 2
    animal.update(visited_locations=[visited_location])
    with pytest.raises(UpdatedFirstPointToChippingPoint):
        change_visited_location(animal, visited_location.id.to_id(), animal.chipping_location_id.to_id())


def test_change_visited_location_negative_sixth(animal):
    with pytest.raises(InvalidID):
        change_visited_location(animal, 0, 1)


def test_change_visited_location_negative_seventh(animal, visited_location):
    animal.visited_locations.append(visited_location)
    with pytest.raises(InvalidID):
        change_visited_location(animal, 1, 0)


def test_change_visited_location_positive(animal, visited_location):
    new_location_id = 69
    animal.update(visited_locations=[visited_location])
    change_visited_location(animal, visited_location.id.to_id(), new_location_id)
    visited_location = animal.get_visited_location(visited_location.id.to_id())
    assert visited_location == AnimalVisitedLocation(id=visited_location.id,
                                                     location_point_id=LocationPointID(new_location_id),
                                                     datetime_of_visit=visited_location.datetime_of_visit,
                                                     animal_id=animal.id)


def test_delete_visited_location_negative(animal, visited_location):
    with pytest.raises(AnimalHasNoCurrentVisitedLocation):
        delete_visited_location(animal, visited_location.id.to_id())


def test_delete_visited_location_positive_first(animal, visited_location):
    animal.update(visited_locations=[visited_location])
    delete_visited_location(animal, visited_location.id.to_id())
    assert visited_location not in animal.visited_locations


def test_delete_visited_location_positive_second(animal, visited_location):
    next_visited_location = AnimalVisitedLocation(id=VisitedLocationID(visited_location.id.value + 5),
                                                  location_point_id=animal.chipping_location_id,
                                                  datetime_of_visit=datetime.utcnow(),
                                                  animal_id=animal.id)
    animal.update(
        visited_locations=[visited_location, next_visited_location],
    )
    delete_visited_location(animal, visited_location.id.to_id())
    assert visited_location not in animal.visited_locations and next_visited_location not in animal.visited_locations
