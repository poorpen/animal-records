from abc import ABC

from src.domain.animal.entities.animal_visited_location import AnimalVisitedLocation

from src.application.common.interfaces.mapper import IMapper

from src.application.location_point.exceptions.location_point import PointNotFound
from src.application.animal.exceptions.animal_visited_location import AnimalVisitedLocationNotFound

from src.application.animal.interfaces.uow.animal_visited_location_uow import IAnimalVisitedLocationUoW
from src.application.animal.interfaces.uow.animal_uow import IAnimalUoW
from src.application.animal.interfaces.uow.location_point_uow import ILocationPointUoW

from src.application.animal.dto.animal_visited_location import \
    AddAnimalVisitedLocationDTO, AnimalVisitedLocationDTO, ChangeAnimalVisitedLocationDTO, SearchParametersDTO, \
    AnimalVisitedLocationDTOs


class VisitedLocationUseCase(ABC):

    def __init__(self, uow: IAnimalUoW | IAnimalVisitedLocationUoW, mapper: IMapper):
        self._uow = uow
        self._mapper = mapper


class GetAnimalVisitedLocations(VisitedLocationUseCase):

    async def __call__(self, search_parameters_dto: SearchParametersDTO) -> AnimalVisitedLocationDTOs:
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
        visited_location_id = await self._uow.animal_repo.update_animal(animal)
        visited_location.id = visited_location_id
        return self._mapper.load(AnimalVisitedLocationDTO, visited_location)


class ChangeVisitedLocationUseCase(VisitedLocationUseCase):

    async def __call__(self, visited_location_dto: ChangeAnimalVisitedLocationDTO) -> AnimalVisitedLocationDTO:
        animal = await self._uow.animal_repo.get_animal_by_id(visited_location_dto.animal_id)
        visited_location = animal.change_visited_location(visited_location_dto.id,
                                                          visited_location_dto.location_point_id)
        await self._uow.animal_repo.update_animal(animal)
        return self._mapper.load(AnimalVisitedLocationDTO, visited_location)


class DeleteVisitedLocationUseCase(VisitedLocationUseCase):

    async def __call__(self, animal_id: int, visited_location_id: int) -> None:
        animal = await self._uow.animal_repo.get_animal_by_id(animal_id)
        animal.delete_visited_location(visited_location_id)
        await self._uow.animal_repo.update_animal(animal)


class AnimalVisitedLocationService:

    def __init__(self, uow: IAnimalVisitedLocationUoW | IAnimalUoW | ILocationPointUoW, mapper: IMapper):
        self._uow = uow
        self._mapper = mapper

    async def get_visited_location(self, search_parameters_dto: SearchParametersDTO) -> AnimalVisitedLocationDTOs:
        return await GetAnimalVisitedLocations(self._uow, self._mapper)(search_parameters_dto)

    async def add_visited_location(self, visited_location_dto: AddAnimalVisitedLocationDTO) -> AnimalVisitedLocationDTO:
        if not await self._uow.location_point_repo.check_exist(visited_location_dto.location_point_id):
            raise PointNotFound(visited_location_dto.location_point_id)
        return await AddVisitedLocationUseCase(self._uow, self._mapper)(visited_location_dto)

    async def change_visited_location(self,
                                      visited_location_dto: ChangeAnimalVisitedLocationDTO
                                      ) -> AnimalVisitedLocationDTO:
        if not await self._uow.animal_repo.check_exist_visited_location(visited_location_dto.id):
            raise AnimalVisitedLocationNotFound(visited_location_dto.id)
        elif not await self._uow.location_point_repo.check_exist(visited_location_dto.location_point_id):
            raise PointNotFound(visited_location_dto.location_point_id)
        return await ChangeVisitedLocationUseCase(self._uow, self._mapper)(visited_location_dto)

    async def delete_visited_location(self, animal_id: int, visited_location_id: int) -> None:
        if not await self._uow.animal_repo.check_exist_visited_location(visited_location_id):
            raise AnimalVisitedLocationNotFound(visited_location_id)
        await DeleteVisitedLocationUseCase(self._uow, self._mapper)(animal_id, visited_location_id)
