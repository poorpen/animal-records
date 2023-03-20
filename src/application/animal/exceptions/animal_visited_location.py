from dataclasses import dataclass

from src.application.animal.exceptions.common import BaseAnimalException


@dataclass
class AnimalVisitedLocationNotFound(BaseAnimalException):
    visited_location_id: int

    def message(self):
        return f'Объект с информацией о посещенной локации с visited_location_id {self.visited_location_id} не найдет'
