from abc import ABC

from src.domain.animal_type.entities.animal_type import AnimalType

from src.application.common.interfaces.mapper import IMapper

from src.application.animal_type.interfaces.uow.animal_type_uow import IAnimalTypeUoW
from src.application.animal_type.dto.animal_type import AnimalTypeDTO, CreateAnimalTypeDTO, ChangeAnimalTypeDTO
from src.application.animal_type.exceptions.animal_type import AnimalTypeAlreadyExist, AnimalTypeNotFound


class AnimalTypeUseCase(ABC):

    def __init__(self, uow: IAnimalTypeUoW, mapper: IMapper):
        self._mapper = mapper
        self._uow = uow


class GetAnimalType(AnimalTypeUseCase):

    async def __call__(self, animal_type_id: int) -> AnimalTypeDTO:
        return await self._uow.animal_type_reader.get_type_by_id(animal_type_id)


class CreateAnimaType(AnimalTypeUseCase):
    async def __call__(self, animal_type_dto: CreateAnimalTypeDTO) -> AnimalTypeDTO:
        animal_type = AnimalType.create(animal_type=animal_type_dto.type)
        try:
            animal_id = await self._uow.animal_type_repo.add_type(animal_type)
            await self._uow.commit()
        except AnimalTypeAlreadyExist:
            await self._uow.rollback()
            raise
        animal_type.id = animal_id
        return self._mapper.load(AnimalTypeDTO, animal_type)


class ChangeAnimalType(AnimalTypeUseCase):
    async def __call__(self, animal_type_dto: ChangeAnimalTypeDTO) -> AnimalTypeDTO:
        animal_type = await self._uow.animal_type_repo.get_type_by_id(animal_type_dto.id)
        animal_type.update(animal_type=animal_type_dto.type)
        try:
            await self._uow.animal_type_repo.change_type(animal_type)
            await self._uow.commit()
        except AnimalTypeAlreadyExist:
            await self._uow.rollback()
            raise
        return self._mapper.load(AnimalTypeDTO, animal_type)


class DeleteAnimalType(AnimalTypeUseCase):

    async def __call__(self, animal_type_id: int) -> None:
        await self._uow.animal_type_repo.delete_type(animal_type_id)
        await self._uow.commit()


class AnimalTypeService:

    def __init__(self, uow: IAnimalTypeUoW, mapper: IMapper):
        self._mapper = mapper
        self._uow = uow

    async def get_animal_type(self, animal_type_id: int) -> AnimalTypeDTO:
        return await GetAnimalType(self._uow, self._mapper)(animal_type_id)

    async def create_animal_type(self, animal_type_dto: CreateAnimalTypeDTO) -> AnimalTypeDTO:
        return await CreateAnimaType(self._uow, self._mapper)(animal_type_dto)

    async def change_animal_type(self, animal_type_dto: ChangeAnimalTypeDTO) -> AnimalTypeDTO:
        return await ChangeAnimalType(self._uow, self._mapper)(animal_type_dto)

    async def delete_animal_type(self, animal_type_id: int) -> None:
        await DeleteAnimalType(self._uow, self._mapper)(animal_type_id)
