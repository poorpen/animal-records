from abc import ABC
from typing import List

from src.domain.animal.entities.animal_visited_location import AnimalVisitedLocation

from src.application.common.interfaces.mapper import IMapper

from src.application.location_point.exceptions.location_point import PointNotFound

from src.application.animal.interfaces.uow.animal_visited_location_uow import IAnimalVisitedLocationUoW
from src.application.animal.interfaces.uow.animal_uow import IAnimalUoW

from src.application.animal.dto.animal_visited_location import \
    AddAnimalVisitedLocationDTO, AnimalVisitedLocationDTO, ChangeAnimalVisitedLocationDTO, SearchParametersDTO


class VisitedLocationUseCase(ABC):

    def __init__(self, uow: IAnimalVisitedLocationUoW | IAnimalUoW, mapper: IMapper):
        self._uow = uow
        self._mapper = mapper


class GetAnimalVisitedLocations(VisitedLocationUseCase):

    async def __call__(self, search_parameters_dto: SearchParametersDTO) -> List[AnimalVisitedLocationDTO]:
        return await self._uow.animal_reader.get_visited_locations(
            animal_id=search_parameters_dto.animal_id,
            start_datetime=search_parameters_dto.start_datetime,
            end_datetime=search_parameters_dto.end_datetime,
            limit=search_parameters_dto.limit,
            offset=search_parameters_dto.offset
        )


class AddVisitedLocationUseCase(VisitedLocationUseCase):

    async def __call__(self, visited_location_dto: AddAnimalVisitedLocationDTO) -> AnimalVisitedLocationDTO:
        visited_location = AnimalVisitedLocation.create(
            location_point_id=visited_location_dto.location_point_id
        )
        animal = await self._uow.animal_repo.get_animal_by_id(visited_location_dto.animal_id)
        animal.add_visited_location(visited_location)
        try:
            visited_location_id = await self._uow.animal_repo.update_animal(animal)
        except PointNotFound:
            await self._uow.rollback()
            raise
        visited_location.id = visited_location_id
        return self._mapper.load(AnimalVisitedLocationDTO, visited_location)


class ChangeVisitedLocationUseCase(VisitedLocationUseCase):

    async def __call__(self, visited_location_dto: ChangeAnimalVisitedLocationDTO) -> AnimalVisitedLocationDTO:
        animal = await self._uow.animal_repo.get_animal_by_id(visited_location_dto.animal_id)
        visited_location = animal.get_visited_location(visited_location_dto.id)
        visited_location.update(
            location_point_id=visited_location_dto.location_point_id
        )
        animal.change_visited_location(visited_location)
        try:
            await self._uow.animal_repo.update_animal(animal)
        except PointNotFound:
            await self._uow.rollback()
            raise
        return self._mapper.load(AnimalVisitedLocationDTO, visited_location)


class DeleteVisitedLocationUseCase(VisitedLocationUseCase):

    async def __call__(self, animal_id: int, visited_location_id: int) -> None:
        animal = await self._uow.animal_repo.get_animal_by_id(animal_id)
        animal.delete_visited_location(visited_location_id)
        await self._uow.animal_repo.update_animal(animal)


class AnimalVisitedLocationService:

    def __init__(self, uow: IAnimalVisitedLocationUoW | IAnimalUoW, mapper: IMapper):
        self._uow = uow
        self._mapper = mapper

    async def get_visited_location(self, search_parameters_dto: SearchParametersDTO) -> List[AnimalVisitedLocationDTO]:
        return await GetAnimalVisitedLocations(self._uow, self._mapper)(search_parameters_dto)

    async def add_visited_location(self, visited_location_dto: AddAnimalVisitedLocationDTO) -> AnimalVisitedLocationDTO:
        return await AddVisitedLocationUseCase(self._uow, self._mapper)(visited_location_dto)

    async def change_visited_location(self,
                                      visited_location_dto: ChangeAnimalVisitedLocationDTO
                                      ) -> AnimalVisitedLocationDTO:
        if await self._uow.animal_repo.check_exist_visited_location(visited_location_dto.id):
            return await ChangeVisitedLocationUseCase(self._uow, self._mapper)(visited_location_dto)

    async def delete_visited_location(self, animal_id: int, visited_location_id: int) -> None:
        if await self._uow.animal_repo.check_exist_visited_location(visited_location_id):
            await DeleteVisitedLocationUseCase(self._uow, self._mapper)(animal_id, visited_location_id)
