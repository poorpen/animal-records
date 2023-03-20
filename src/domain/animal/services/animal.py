from datetime import datetime

from src.domain.animal.exceptions.animal import AttemptToResurrectAnimal, ChippingLocationEqualFirstLocation

from src.domain.animal.enums import LifeStatus
from src.domain.animal.entities.animal import Animal
from src.domain.animal.values_objects.animal import ChippingLocationID


def set_death_datetime(animal: Animal) -> None:
    if animal.life_status.to_enum() == LifeStatus.DEAD:
        animal.death_datetime = datetime.utcnow()


def check_life_status_conflict(animal: Animal, life_status: str):
    if animal.life_status.to_enum() == LifeStatus.DEAD and life_status == 'ALIVE':
        raise AttemptToResurrectAnimal(animal.id.to_id())


def check_chipping_location(animal: Animal, chipping_location: ChippingLocationID):
    if animal.visited_locations:
        first_visited_location = animal.visited_locations[0]
        if first_visited_location and first_visited_location.location_point_id == chipping_location:
            raise ChippingLocationEqualFirstLocation(animal.id.to_id(), chipping_location.to_id())
