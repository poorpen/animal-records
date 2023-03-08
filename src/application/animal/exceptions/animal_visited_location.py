from dataclasses import dataclass

from src.application.common.exceptions.application import ApplicationException


@dataclass
class AnimalVisitedLocationNotFound(ApplicationException):
    visited_location_id: int

    def message(self):
        return f'Объект с информацией о посещенной локации с visited_location_id {self.visited_location_id} не найдет'
