from dataclasses import dataclass

from src.application.common.exceptions.application import ApplicationException


@dataclass
class PointNotFound(ApplicationException):
    location_point_id: int

    def message(self):
        return f'Точка с location_point_id {self.location_point_id} не найдена'


@dataclass
class PointAlreadyExist(ApplicationException):
    latitude: float
    longitude: float

    def message(self):
        return f"Точка локации с latitude {self.latitude} и longitude {self.longitude} уже существует"


@dataclass
class AnimalAssociatedWithPoint(ApplicationException):
    location_point_id: int

    def message(self):
        return f'Точка локации с location_point_id {self.location_point_id} c животным'

