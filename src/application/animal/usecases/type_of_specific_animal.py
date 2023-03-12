from abc import ABC

from src.domain.animal.services.type_of_specific_animal import add_animal_type, change_animal_type, delete_animal_type

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
        animal = await self._uow.animal_repo.get_animal_by_id(animal_type_dto.animal_id)
        add_animal_type(animal, animal_type_dto.animal_type_id)
        try:
            updated_animal = await self._uow.animal_repo.update_animal(animal)
            await self._uow.commit()
        except AnimalTypeNotFound:
            await self._uow.rollback()
            raise
        return self._mapper.load(AnimalDTO, updated_animal)


class ChangeTypeOfSpecificAnimal(TypeOfSpecificAnimalUseCse):

    async def __call__(self, animal_type_dto: ChangeTypeOfSpecificAnimalDTO) -> AnimalDTO:
        animal = await self._uow.animal_repo.get_animal_by_id(animal_type_dto.animal_id)
        change_animal_type(animal, animal_type_dto.old_type_id, animal_type_dto.new_type_id)
        try:
            updated_animal = await self._uow.animal_repo.update_animal(animal)
            await self._uow.commit()
        except AnimalTypeNotFound:
            await self._uow.rollback()
            raise
        return self._mapper.load(AnimalDTO, updated_animal)


class DeleteTypeOfSpecificAnimal(TypeOfSpecificAnimalUseCse):

    async def __call__(self, animal_id: int, type_id: int) -> AnimalDTO:
        animal = await self._uow.animal_repo.get_animal_by_id(animal_id)
        delete_animal_type(animal, type_id)
        updated_animal = await self._uow.animal_repo.update_animal(animal)
        await self._uow.commit()
        return self._mapper.load(AnimalDTO, updated_animal)


class TypeOfSpecificAnimalService:

    def __init__(self, uow: IAnimalUoW | IAnimalTypeUoW, mapper: IMapper):
        self._uow = uow
        self._mapper = mapper

    async def add_type(self, animal_type_dto: AddTypeOfSpecificAnimalDTO):
        await AddTypeToSpecificAnimal(self._uow, self._mapper)(animal_type_dto)

    async def change_type(self, animal_type_dto: ChangeTypeOfSpecificAnimalDTO):
        if not self._uow.animal_type_repo.check_exist(animal_type_dto.old_type_id):
            raise AnimalTypeNotFound(animal_type_dto.old_type_id)
        await ChangeTypeOfSpecificAnimal(self._uow, self._mapper)(animal_type_dto)

    async def delete_type(self, animal_id: int, type_id: int):
        if not self._uow.animal_type_repo.check_exist(type_id):
            raise AnimalTypeNotFound(type_id)
        await DeleteTypeOfSpecificAnimal(self._uow, self._mapper)(animal_id, type_id)
