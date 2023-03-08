from dataclasses import dataclass

from src.domain.common.exceptions.domain import DomainException


@dataclass
class AnimalHasNoCurrentVisitedLocation(DomainException):
    animal_id: int
    visited_location_id: int

    def message(self):
        return f'У животного с animal_id {self.animal_id} нет объекта с информацией о посещенной ' \
               f'точке локации с visited_location_id {self.visited_location_id}'


@dataclass
class BaseLocationPointException(DomainException):
    animal_id: int
    location_point_id: int


class AnimalNowInThisPoint(BaseLocationPointException):
    def message(self):
        return f'Животное с animal_id {self.animal_id} уже находиться ' \
               f'в точке локации с location_point_id {self.location_point_id}'


class LocationPointEqualToChippingLocation(BaseLocationPointException):

    def message(self):
        return f'Попытка добавить животному с animal_id {self.animal_id} ' \
               f'точку локации с location_point_id {self.location_point_id} равную chipping_location_id'


class UpdatedFirstPointToChippingPoint(BaseLocationPointException):

    def message(self):
        return f'Попытка обновление первой посещенной точки локации у животного с animal_id {self.animal_id} на другу ' \
               f'точку локации с location_point_id {self.location_point_id}, которая совпадает с chipping_location_id'


class UpdateToSameLocationPoint(BaseLocationPointException):

    def message(self):
        return f'Попытка обновления посещенной точки локации у животного с animal_id {self.animal_id} ' \
               f'на ту же точку локации с location_point_id {self.location_point_id} '


class NextOfPreviousEqualThisLocation(BaseLocationPointException):

    def message(self):
        return f'Попытка обновления точки локации на другую точку локации с location_point_id {self.location_point_id}, ' \
               f'которая совпадает со следующей и/или с предыдущей точками'
