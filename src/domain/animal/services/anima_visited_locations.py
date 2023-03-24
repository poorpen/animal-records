from datetime import datetime

from src.domain.animal.enums import LifeStatus
from src.domain.animal.entities.animal_visited_location import AnimalVisitedLocation
from src.domain.animal.entities.animal import Animal

from src.domain.animal.exceptions.animal_visited_location import \
    LocationPointEqualToChippingLocation, AnimalNowInThisPoint, NextOfPreviousEqualThisLocation, \
    UpdateToSameLocationPoint, UpdatedFirstPointToChippingPoint
from src.domain.animal.exceptions.animal import AnimalIsDead

from src.domain.animal.values_objects.animal_visited_location import LocationPointID


def add_visited_location(animal: Animal, location_point_id: int):
    location_point_vo = LocationPointID(location_point_id)
    if animal.life_status.to_enum() == LifeStatus.DEAD:
        raise AnimalIsDead(animal.id)
    elif not animal.visited_locations and animal.chipping_location_id.to_id() == location_point_vo.to_id():
        raise LocationPointEqualToChippingLocation(animal.id, location_point_vo)
    elif animal.visited_locations:
        if animal.visited_locations[-1].location_point_id.to_id() == location_point_vo.to_id():
            raise AnimalNowInThisPoint(animal.id, location_point_vo)

    visited_location = AnimalVisitedLocation.create(location_point_id=location_point_vo,
                                                    animal_id=animal.id,
                                                    datetime_of_visit=datetime.utcnow())
    animal.update(visited_locations=[visited_location])


def change_visited_location(animal: Animal, visited_location_id: int, new_location_point_id: int) -> None:
    location_point_vo = LocationPointID(new_location_point_id)
    visited_location = animal.get_visited_location(visited_location_id)
    location_index = animal.visited_locations.index(visited_location)
    if visited_location.location_point_id.to_id() == location_point_vo.to_id():
        raise UpdateToSameLocationPoint(animal.id, visited_location.location_point_id)

    if location_index > 0:
        previous_element = animal.visited_locations[location_index - 1]
        if previous_element.location_point_id.to_id() == location_point_vo.to_id():
            raise NextOfPreviousEqualThisLocation(animal.id, visited_location.location_point_id)

    if location_index < len(animal.visited_locations) - 1:
        next_element = animal.visited_locations[location_index + 1]
        if next_element.location_point_id.to_id() == location_point_vo.to_id():
            raise NextOfPreviousEqualThisLocation(animal.id, visited_location.location_point_id)

    if location_index == 0 and location_point_vo.to_id() == animal.chipping_location_id.to_id():
        raise UpdatedFirstPointToChippingPoint(animal.id, visited_location.location_point_id)

    animal.visited_locations[location_index].update(location_point_id=location_point_vo)


def delete_visited_location(animal: Animal, visited_location_id: int) -> None:
    visited_location = animal.get_visited_location(visited_location_id)

    index_visited_location = animal.visited_locations.index(visited_location)

    if index_visited_location < len(animal.visited_locations) - 1:
        next_visited_location = animal.visited_locations[index_visited_location + 1]

        if index_visited_location == 0 and \
                next_visited_location.location_point_id.to_id() == animal.chipping_location_id.to_id():
            animal.visited_locations.remove(next_visited_location)
    animal.visited_locations.remove(visited_location)
