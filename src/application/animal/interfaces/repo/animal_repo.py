from datetime import datetime
from typing import Protocol

from src.domain.animal.value_objects.gender import Gender
from src.domain.animal.value_objects.life_status import LifeStatus
from src.domain.animal.entities.animal import Animal

from src.application.animal.dto.animal import AnimalDTO, AnimalDTOs


class IAnimalRepo(Protocol):

    async def get_animal_by_id(self, animal_id: int) -> Animal:
        raise NotImplementedError

    async def add_animal(self, animal: Animal) -> int:
        raise NotImplementedError

    async def update_animal(self, animal: Animal) -> None:
        raise NotImplementedError

    async def delete_animal(self, animal_id: int) -> None:
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
