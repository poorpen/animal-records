from typing import Protocol

from src.domain.animal_type.value_objects import AnimalTypeID
from src.domain.animal_type.entities.animal_type import AnimalType

from src.application.animal_type.dto.animal_type import AnimalTypeDTO


class IAnimalTypeRepo(Protocol):

    async def get_type_by_id(self, animal_type_id: AnimalTypeID) -> AnimalType:
        raise NotImplementedError

    async def add_type(self, animal_type: AnimalType) -> None:
        raise NotImplementedError

    async def change_type(self, animal_type: AnimalType) -> None:
        raise NotImplementedError

    async def delete_type(self, animal_type_id: AnimalTypeID) -> None:
        raise NotImplementedError


class IAnimalTypeReader(Protocol):

    async def get_type_by_id(self, animal_type_id: int) -> AnimalTypeDTO:
        raise NotImplementedError
