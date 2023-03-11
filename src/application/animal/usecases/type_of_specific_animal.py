from abc import ABC

from src.domain.animal.entities.type_of_specific_animal import TypeOfSpecificAnimal

from src.application.common.interfaces.mapper import IMapper

from src.application.animal_type.exceptions.animal_type import AnimalTypeNotFound

from src.application.animal.interfaces.uow.animal_uow import IAnimalUoW
from src.application.animal.interfaces.uow.animal_type_uow import IAnimalTypeUoW
from src.application.animal.dto.type_of_specific_animal import ChangeTypeOfSpecificAnimalDTO, \
    AddTypeOfSpecificAnimalDTO
from src.application.animal.dto.animal import AnimalDTO


class TypeOfSpecificAnimalUseCse(ABC):

    def __init__(self, uow: IAnimalUoW | IAnimalTypeUoW, mapper: IMapper):
        self._uow = uow
        self._mapper = mapper


class AddTypeToSpecificAnimal(TypeOfSpecificAnimalUseCse):

    async def __call__(self, animal_type_dto: AddTypeOfSpecificAnimalDTO) -> AnimalDTO:
        type_of_specific_animal = TypeOfSpecificAnimal.create(animal_id=animal_type_dto.animal_id,
                                                              animal_type_id=animal_type_dto.animal_type_id)
        animal = await self._uow.animal_repo.get_animal_by_id(animal_type_dto.animal_id)
        animal.add_animal_type(type_of_specific_animal)
        try:
            await self._uow.animal_repo.update_animal(animal)
        except AnimalTypeNotFound:
            await self._uow.rollback()
            raise
        return self._mapper.load(AnimalDTO, animal)


class ChangeTypeOfSpecificAnimal(TypeOfSpecificAnimalUseCse):

    async def __call__(self, animal_type_dto: ChangeTypeOfSpecificAnimalDTO) -> AnimalDTO:
        animal = await self._uow.animal_repo.get_animal_by_id(animal_type_dto.animal_id)
        animal.change_animal_type(animal_type_dto.old_type_id, animal_type_dto.new_type_id)
        try:
            await self._uow.animal_repo.update_animal(animal)
        except AnimalTypeNotFound:
            await self._uow.rollback()
            raise
        return self._mapper.load(AnimalDTO, animal)


class DeleteTypeOfSpecificAnimal(TypeOfSpecificAnimalUseCse):

    async def __call__(self, animal_id: int, type_id: int) -> AnimalDTO:
        animal = await self._uow.animal_repo.get_animal_by_id(animal_id)
        animal.delete_animal_type(type_id)
        await self._uow.animal_repo.update_animal(animal)
        return self._mapper.load(AnimalDTO, animal)


class TypeOfSpecificAnimalService:

    def __init__(self, uow: IAnimalUoW | IAnimalTypeUoW, mapper: IMapper):
        self._uow = uow
        self._mapper = mapper

    async def add_type(self, animal_type_dto: AddTypeOfSpecificAnimalDTO):
        if not self._uow.animal_type_repo.check_exist(animal_type_dto.animal_type_id):
            raise AnimalTypeNotFound(animal_type_dto.animal_type_id)
        await AddTypeToSpecificAnimal(self._uow, self._mapper)(animal_type_dto)

    async def change_type(self, animal_type_dto: ChangeTypeOfSpecificAnimalDTO):
        if not self._uow.animal_type_repo.check_exist(animal_type_dto.old_type_id):
            raise AnimalTypeNotFound(animal_type_dto.old_type_id)
        elif not self._uow.animal_type_repo.check_exist(animal_type_dto.new_type_id):
            raise AnimalTypeNotFound(animal_type_dto.new_type_id)
        await ChangeTypeOfSpecificAnimal(self._uow, self._mapper)(animal_type_dto)

    async def delete_type(self, animal_id: int, type_id: int):
        if not self._uow.animal_type_repo.check_exist(type_id):
            raise AnimalTypeNotFound(type_id)
        await DeleteTypeOfSpecificAnimal(self._uow, self._mapper)(animal_id, type_id)
