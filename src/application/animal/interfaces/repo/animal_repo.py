from datetime import datetime
from typing import Protocol

from src.domain.animal.enums import LifeStatus, Gender
from src.domain.animal.values_objects.common import AnimalID
from src.domain.animal.entities.animal import Animal

from src.application.animal.dto.animal import AnimalDTO, AnimalDTOs


class IAnimalRepo(Protocol):

    async def get_animal_by_id(self, animal_id: AnimalID) -> Animal:
        raise NotImplementedError

    async def add_animal(self, animal: Animal) -> int:
        raise NotImplementedError

    async def update_animal(self, animal: Animal) -> Animal:
        raise NotImplementedError

    async def delete_animal(self, animal_id: AnimalID) -> None:
        raise NotImplementedError


class IAnimalReader(Protocol):

    async def get_animal_by_id(self, animal_id: int) -> AnimalDTO:
        raise NotImplementedError

    async def search_anima(self,
                           start_datetime: datetime,
                           end_datetime: datetime,
                           chipper_id: int,
                           chipping_location_id: int,
                           life_status: LifeStatus,
                           gender: Gender,
                           limit: int,
                           offset: int
                           ) -> AnimalDTOs:
        raise NotImplementedError
