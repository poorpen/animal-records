import pytest

from datetime import datetime

from src.domain.animal.exceptions.animal_visited_location import LocationPointEqualToChippingLocation, \
    AnimalNowInThisPoint, UpdateToSameLocationPoint, NextOfPreviousEqualThisLocation, AnimalHasNoCurrentVisitedLocation, \
    UpdatedFirstPointToChippingPoint
from src.domain.animal.exceptions.animal import AnimalIsDead

from src.domain.animal.value_objects.life_status import LifeStatus
from src.domain.animal.entities.animal_visited_location import AnimalVisitedLocation

from test.domain.entities.common import animal


@pytest.fixture()
def visited_location():
    return AnimalVisitedLocation(id=1, location_point_id=4, datetime_of_visit=datetime.utcnow())


def test_add_visited_location_negative_first(animal, visited_location):
    animal.life_status = LifeStatus.DEAD
    with pytest.raises(AnimalIsDead):
        animal.add_visited_location(visited_location)


def test_add_visited_location_negative_second(animal, visited_location):
    visited_location.location_point_id = animal.chipping_location_id
    with pytest.raises(LocationPointEqualToChippingLocation):
        animal.add_visited_location(visited_location)


def test_add_visited_location_negative_third(animal, visited_location):
    visited_location.location_point_id = visited_location.location_point_id + 2
    animal.visited_locations.append(visited_location)
    with pytest.raises(AnimalNowInThisPoint):
        animal.add_visited_location(visited_location)


def test_add_visited_location_positive(animal, visited_location):
    visited_location.location_point_id = visited_location.location_point_id + 2
    animal.visited_locations.append(visited_location)
    assert visited_location in animal.visited_locations


def test_change_visited_location_negative_first(animal, visited_location):
    visited_location.location_point_id = 6
    with pytest.raises(AnimalHasNoCurrentVisitedLocation):
        animal.change_visited_location(visited_location.id, visited_location.location_point_id)


def test_change_visited_location_negative_second(animal, visited_location):
    visited_location.location_point_id = 6
    animal.add_visited_location(visited_location)
    with pytest.raises(UpdateToSameLocationPoint):
        animal.change_visited_location(visited_location.id, visited_location.location_point_id)


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
        animal.change_visited_location(visited_location_id, visited_location.location_point_id)


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
        animal.change_visited_location(visited_location_id, visited_location.location_point_id)


def test_change_visited_location_negative_fifth(animal, visited_location):
    visited_location.location_point_id += 2
    animal.add_visited_location(visited_location)
    with pytest.raises(UpdatedFirstPointToChippingPoint):
        animal.change_visited_location(visited_location.id, animal.chipping_location_id)


def test_change_visited_location_positive(animal, visited_location):
    new_location_id = 69
    animal.add_visited_location(visited_location)
    visited_location = animal.change_visited_location(visited_location.id, new_location_id)
    assert visited_location == AnimalVisitedLocation(id=visited_location.id, location_point_id=new_location_id,
                                                     datetime_of_visit=visited_location.datetime_of_visit)


def test_delete_visited_location_negative(animal, visited_location):
    with pytest.raises(AnimalHasNoCurrentVisitedLocation):
        animal.delete_visited_location(visited_location.id)


def test_delete_visited_location_positive_first(animal, visited_location):
    animal.add_visited_location(visited_location)
    animal.delete_visited_location(visited_location.id)
    assert visited_location not in animal.visited_locations


def test_delete_visited_location_positive_second(animal, visited_location):
    next_visited_location = AnimalVisitedLocation(id=visited_location.id + 5,
                                                  location_point_id=animal.chipping_location_id,
                                                  datetime_of_visit=datetime.utcnow())
    animal.update(
        visited_locations=[visited_location, next_visited_location],
    )
    animal.delete_visited_location(visited_location.id)
    assert visited_location not in animal.visited_locations and next_visited_location not in animal.visited_locations
