from dataclasses import dataclass

from src.domain.location_point.value_objects import LocationPointID

from src.domain.animal.values_objects.common import AnimalID
from src.domain.animal.values_objects.animal_visited_location import VisitedLocationID

from src.domain.animal.exceptions.common import BaseAnimalDomainException


@dataclass
class AnimalHasNoCurrentVisitedLocation(BaseAnimalDomainException):
    animal_id: AnimalID
    visited_location_id: VisitedLocationID

    def message(self):
        return f'У животного с animal_id {self.animal_id.to_id()} нет объекта с информацией о посещенной ' \
               f'точке локации с visited_location_id {self.visited_location_id.to_id()}'


@dataclass
class BaseLocationPointException(BaseAnimalDomainException):
    animal_id: AnimalID
    location_point_id: LocationPointID


class AnimalNowInThisPoint(BaseLocationPointException):
    def message(self):
        return f'Животное с animal_id {self.animal_id.to_id()} уже находиться ' \
               f'в точке локации с location_point_id {self.location_point_id.to_id()}'


class LocationPointEqualToChippingLocation(BaseLocationPointException):

    def message(self):
        return f'Попытка добавить животному с animal_id {self.animal_id.to_id()} ' \
               f'точку локации с location_point_id {self.location_point_id.to_id()} равную chipping_location_id'


class UpdatedFirstPointToChippingPoint(BaseLocationPointException):

    def message(self):
        return f'Попытка обновление первой посещенной точки локации у животного с animal_id {self.animal_id.to_id()} на другу ' \
               f'точку локации с location_point_id {self.location_point_id.to_id()}, которая совпадает с chipping_location_id'


class UpdateToSameLocationPoint(BaseLocationPointException):

    def message(self):
        return f'Попытка обновления посещенной точки локации у животного с animal_id {self.animal_id.to_id()} ' \
               f'на ту же точку локации с location_point_id {self.location_point_id.to_id()} '


class NextOfPreviousEqualThisLocation(BaseLocationPointException):

    def message(self):
        return f'Попытка обновления точки локации на другую точку локации с location_point_id {self.location_point_id.to_id()}, ' \
               f'которая совпадает со следующей и/или с предыдущей точками'
