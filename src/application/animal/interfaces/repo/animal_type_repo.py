from typing import Protocol

from src.domain.animal.values_objects.type_of_specific_animal import AnimalTypeID


class IAnimalTypeRepo(Protocol):

    async def check_exist(self, animal_type_id: AnimalTypeID) -> bool:
        raise NotImplementedError
