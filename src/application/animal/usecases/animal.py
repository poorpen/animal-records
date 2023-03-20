from abc import ABC

from src.domain.animal.values_objects.common import AnimalID
from src.domain.animal.values_objects.animal import \
    ChippingLocationID, LifeStatusVO, GenderVO, Height, Length, Weight, ChipperID

from src.domain.animal.services.animal import \
    set_death_datetime, check_life_status_conflict, check_chipping_location
from src.domain.animal.entities.animal import Animal

from src.application.common.interfaces.mapper import IMapper

from src.application.animal_type.exceptions.animal_type import AnimalTypeNotFound
from src.application.account.exceptions.account import AccountNotFoundByID
from src.application.location_point.exceptions.location_point import PointNotFound

from src.application.animal.interfaces.uow.animal_uow import IAnimalUoW
from src.application.animal.dto.animal import \
    AnimalDTO, CreateAnimalDTO, SearchParametersDTO, UpdateAnimalDTO, AnimalDTOs
from src.application.animal.exceptions.animal import AnimalHaveDuplicateTypes, AnimalHaveVisitedLocation


class AnimalUseCase(ABC):

    def __init__(self, uow: IAnimalUoW, mapper: IMapper):
        self._uow = uow
        self._mapper = mapper


class CreateAnimal(AnimalUseCase):

    async def __call__(self, animal_dto: CreateAnimalDTO) -> AnimalDTO:
        animal = Animal.create(
            animal_types=animal_dto.animal_types,
            weight=Weight(animal_dto.weight),
            length=Length(animal_dto.length),
            height=Height(animal_dto.height),
            gender=GenderVO(animal_dto.gender),
            chipping_location_id=ChippingLocationID(animal_dto.chipping_location_id),
            chipper_id=ChipperID(animal_dto.chipper_id),
        )
        type_of_specific_animal = animal.check_duplicate_types()
        if type_of_specific_animal:
            raise AnimalHaveDuplicateTypes(type_of_specific_animal.animal_type_id.to_id())
        try:
            updated_animal = await self._uow.animal_repo.add_animal(animal)
            await self._uow.commit()
        except (AnimalTypeNotFound, AccountNotFoundByID, PointNotFound):
            await self._uow.rollback()
            raise
        return self._mapper.load(AnimalDTO, updated_animal)


class UpdateAnimal(AnimalUseCase):

    async def __call__(self, animal_dto: UpdateAnimalDTO) -> AnimalDTO:
        animal = await self._uow.animal_repo.get_animal_by_id(AnimalID(animal_dto.id))
        check_life_status_conflict(animal, animal_dto.life_status)
        check_chipping_location(animal, animal_dto.chipping_location_id)
        animal.update(
            weight=Weight(animal_dto.weight),
            length=Length(animal_dto.length),
            height=Height(animal_dto.height),
            gender=GenderVO(animal_dto.gender),
            life_status=LifeStatusVO(animal_dto.life_status),
            chipper_id=ChipperID(animal_dto.chipper_id),
            chipping_location_id=ChippingLocationID(animal_dto.chipping_location_id)
        )
        set_death_datetime(animal)
        try:
            await self._uow.animal_repo.update_animal(animal)
            await self._uow.commit()
        except (AccountNotFoundByID, PointNotFound):
            await self._uow.rollback()
            raise
        return self._mapper.load(AnimalDTO, animal)


class GetAnimal(AnimalUseCase):

    async def __call__(self, animal_id: int) -> AnimalDTO:
        return await self._uow.animal_reader.get_animal_by_id(animal_id)


class SearchAnimal(AnimalUseCase):

    async def __call__(self, search_parameters_dto: SearchParametersDTO) -> AnimalDTOs:
        return await self._uow.animal_reader.search_anima(
            start_datetime=search_parameters_dto.start_datetime,
            end_datetime=search_parameters_dto.end_datetime,
            chipper_id=search_parameters_dto.chipper_id,
            chipping_location_id=search_parameters_dto.chipping_location_id,
            life_status=search_parameters_dto.life_status,
            gender=search_parameters_dto.gender,
            limit=search_parameters_dto.limit,
            offset=search_parameters_dto.offset
        )


class DeleteAnimal(AnimalUseCase):

    async def __call__(self, animal_id: int) -> None:
        try:
            await self._uow.animal_repo.delete_animal(AnimalID(animal_id))
            await self._uow.commit()
        except AnimalHaveVisitedLocation:
            await self._uow.rollback()
            raise


class AnimalService:

    def __init__(self, uow: IAnimalUoW, mapper: IMapper):
        self._uow = uow
        self._mapper = mapper

    async def create_animal(self, animal_dto: CreateAnimalDTO) -> AnimalDTO:
        return await CreateAnimal(self._uow, self._mapper)(animal_dto)

    async def update_animal(self, animal_dto: UpdateAnimalDTO) -> AnimalDTO:
        return await UpdateAnimal(self._uow, self._mapper)(animal_dto)

    async def get_animal(self, animal_id: int) -> AnimalDTO:
        return await GetAnimal(self._uow, self._mapper)(animal_id)

    async def search_animal(self, search_parameters_dto: SearchParametersDTO) -> AnimalDTOs:
        return await SearchAnimal(self._uow, self._mapper)(search_parameters_dto)

    async def delete_animal(self, animal_id: int) -> None:
        return await DeleteAnimal(self._uow, self._mapper)(animal_id)
