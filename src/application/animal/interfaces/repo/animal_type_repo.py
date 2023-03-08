from typing import Protocol


class IAnimalTypeRepo(Protocol):

    async def check_exist(self, animal_type_id) -> bool:
        raise NotImplementedError
