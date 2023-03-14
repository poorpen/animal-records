from abc import ABC

from src.domain.animal.services.anima_visited_locations import add_visited_location, change_visited_location, \
    delete_visited_location

from src.application.common.interfaces.mapper import IMapper

from src.application.location_point.exceptions.location_point import PointNotFound
from src.application.animal.exceptions.animal_visited_location import AnimalVisitedLocationNotFound

from src.application.animal.interfaces.uow.animal_visited_location_uow import IAnimalVisitedLocationUoW
from src.application.animal.interfaces.uow.animal_uow import IAnimalUoW

from src.application.animal.dto.animal import AnimalID
from src.application.animal.dto.animal_visited_location import \
    AddAnimalVisitedLocationDTO, AnimalVisitedLocationDTO, ChangeAnimalVisitedLocationDTO, SearchParametersDTO, \
    AnimalVisitedLocationDTOs, AnimalVisitedLocationID


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
        animal = await self._uow.animal_repo.get_animal_by_id(visited_location_dto.animal_id)

        add_visited_location(animal, visited_location_dto.location_point_id)

        updated_animal = await self._uow.animal_repo.update_animal(animal)
        await self._uow.commit()
        return self._mapper.load(AnimalVisitedLocationDTO, updated_animal.visited_locations[-1])


class ChangeVisitedLocationUseCase(VisitedLocationUseCase):

    async def __call__(self, visited_location_dto: ChangeAnimalVisitedLocationDTO) -> AnimalVisitedLocationDTO:
        animal = await self._uow.animal_repo.get_animal_by_id(visited_location_dto.animal_id)

        change_visited_location(animal, visited_location_dto.id, visited_location_dto.location_point_id)
        visited_location = animal.get_visited_location(visited_location_dto.id)

        try:
            await self._uow.animal_repo.update_animal(animal)
            await self._uow.commit()
        except PointNotFound:
            await self._uow.rollback()
            raise
        return self._mapper.load(AnimalVisitedLocationDTO, visited_location)


class DeleteVisitedLocationUseCase(VisitedLocationUseCase):

    async def __call__(self, animal: AnimalID, visited_location: AnimalVisitedLocationID) -> None:
        animal = await self._uow.animal_repo.get_animal_by_id(animal.id)
        delete_visited_location(animal, visited_location.id)
        await self._uow.animal_repo.update_animal(animal)
        await self._uow.commit()


class AnimalVisitedLocationService:

    def __init__(self, uow: IAnimalVisitedLocationUoW | IAnimalUoW, mapper: IMapper):
        self._uow = uow
        self._mapper = mapper

    async def get_visited_location(self, search_parameters_dto: SearchParametersDTO) -> AnimalVisitedLocationDTOs:
        return await GetAnimalVisitedLocations(self._uow, self._mapper)(search_parameters_dto)

    async def add_visited_location(self, visited_location_dto: AddAnimalVisitedLocationDTO) -> AnimalVisitedLocationDTO:

        return await AddVisitedLocationUseCase(self._uow, self._mapper)(visited_location_dto)

    async def change_visited_location(self,
                                      visited_location_dto: ChangeAnimalVisitedLocationDTO
                                      ) -> AnimalVisitedLocationDTO:
        if not self._uow.animal_repo.check_exist_visited_location(visited_location_dto.location_point_id):
            raise AnimalVisitedLocationNotFound(visited_location_dto.id)
        return await ChangeVisitedLocationUseCase(self._uow, self._mapper)(visited_location_dto)

    async def delete_visited_location(self, animal: AnimalID, visited_location: AnimalVisitedLocationID) -> None:
        if not self._uow.animal_repo.check_exist_visited_location(visited_location.id):
            raise AnimalVisitedLocationNotFound(visited_location.id)
        await DeleteVisitedLocationUseCase(self._uow, self._mapper)(animal, visited_location)
