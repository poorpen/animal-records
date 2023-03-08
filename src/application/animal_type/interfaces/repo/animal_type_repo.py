from typing import Protocol

from src.domain.animal_type.entities.animal_type import AnimalType

from src.application.animal_type.dto.animal_type import AnimalTypeDTO


class IAnimalTypeRepo(Protocol):

    async def get_type_by_id(self, animal_type_id: int) -> AnimalType:
        raise NotImplementedError

    async def add_type(self, animal_type: AnimalType) -> None:
        raise NotImplementedError

    async def change_type(self, animal_type: AnimalType) -> None:
        raise NotImplementedError

    async def delete_type(self, animal_type_id: int) -> None:
        raise NotImplementedError

    async def check_exist(self, animal_type_id) -> bool:
        raise NotImplementedError


class IAnimalTypeReader(Protocol):

    async def get_type_by_id(self, animal_type_id: int) -> AnimalTypeDTO:
        raise NotImplementedError
