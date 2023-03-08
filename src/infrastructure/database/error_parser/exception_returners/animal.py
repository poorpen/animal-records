from src.domain.animal.entities.type_of_specific_animal import TypeOfSpecificAnimal
from src.domain.animal.entities.animal_visited_location import AnimalVisitedLocation
from src.domain.animal.entities.animal import Animal

from src.application.animal.exceptions.animal import AnimalNotFound
from src.application.animal_type.exceptions.animal_type import AnimalTypeNotFound
from src.application.account.exceptions.account import AccountNotFoundByID
from src.application.location_point.exceptions.location_point import PointNotFound
from src.application.animal.exceptions.animal_visited_location import AnimalVisitedLocationNotFound


def animal_type_not_found(animal_type: TypeOfSpecificAnimal):
    return AnimalTypeNotFound(animal_type.animal_type_id)


def chipper_not_found(animal: Animal):
    return AccountNotFoundByID(animal.chipper_id)


def location_point_not_found(anima: Animal):
    return PointNotFound(anima.chipping_location_id)


def animal_visited_location_not_found(visited_location: AnimalVisitedLocation):
    return AnimalVisitedLocationNotFound(visited_location.id)