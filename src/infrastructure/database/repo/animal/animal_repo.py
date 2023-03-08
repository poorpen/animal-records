from datetime import datetime
from typing import List

from sqlalchemy import exists, insert, select, delete
from sqlalchemy.exc import IntegrityError

from src.domain.animal.value_objects.gender import Gender
from src.domain.animal.value_objects.life_status import LifeStatus
from src.domain.animal.entities.animal import Animal
from src.domain.animal.entities.type_of_specific_animal import TypeOfSpecificAnimal

from src.application.animal.dto.animal import AnimalDTO
from src.application.animal.dto.animal_visited_location import AnimalVisitedLocationDTO
from src.application.animal.exceptions.animal import AnimalNotFound
from src.application.animal.interfaces.repo.animal_visited_location_repo import IAnimalVisitedLocationRepo, \
    IAnimalVisitedLocationReader
from src.application.animal.interfaces.repo.animal_repo import IAnimalRepo, IAnimalReader
from src.infrastructure.database.models import TypeOfSpecificAnimalDB

from src.infrastructure.database.repo.common.base_repo import SQLAlchemyRepo
from src.infrastructure.database.models.animal import AnimalDB
from src.infrastructure.database.models.animal_visited_location import AnimalVisitedLocationDB
from src.infrastructure.database.repo.common.base_query_bilder import BaseQueryBuilder


class AnimalRepo(SQLAlchemyRepo, IAnimalRepo, IAnimalVisitedLocationRepo):

    async def add_animal(self, animal: Animal) -> int:
        sql = insert(AnimalDB).values(weight=animal.weight,
                                      length=animal.length,
                                      height=animal.height,
                                      gender=animal.gender,
                                      life_status=animal.life_status,
                                      chipping_datetime=animal.chipping_datetime,
                                      chipping_location_id=animal.chipping_location_id,
                                      chipper_id=animal.chipper_id,
                                      death_datetime=animal.death_datetime).returning(AnimalDB.id)

        try:
            result = await self._session.execute(sql)
        except IntegrityError as exc:
            raise self._error_parser.parse_error(animal, exc)

        row_id = result.scalar()

        await self._add_animal_types(row_id, animal.animal_types)

        return row_id

    async def get_animal_by_id(self, animal_id: int) -> Animal:
        sql = select(AnimalDTO).where(AnimalDTO.id == animal_id)
        result = await self._session.execute(sql)
        model = result.scalar()
        if not model:
            raise AnimalNotFound(animal_id)
        return self._mapper.load(Animal, model)

    async def update_animal(self, animal: Animal) -> None:
        anima_db = self._mapper.load(AnimalDB, animal)
        try:
            await self._session.merge(anima_db)
        except IntegrityError as exc:
            raise self._error_parser.parse_error(animal, exc)

    async def delete_animal(self, animal_id: int) -> None:
        sql = delete(AnimalDB).where(AnimalDTO.id == animal_id).returning(AnimalDB.id)
        result = await self._session.execute(sql)
        deleted_row_id = result.scalar()
        if not deleted_row_id:
            raise AnimalNotFound(animal_id)

    async def check_exist_visited_location(self, visited_location_id: int) -> bool:
        sql = exists(AnimalVisitedLocationDB.id).where(AnimalVisitedLocationDB.id == visited_location_id).select()
        result = await self._session.execute(sql)
        check_result = result.scalar()
        return check_result

    async def _add_animal_types(self, animal_id: int, current_animal_type: List[TypeOfSpecificAnimal]):
        for this_animal_type in current_animal_type:
            try:
                await self._session.execute(
                    insert(TypeOfSpecificAnimalDB).values(animal_id=animal_id, animal_type_id=this_animal_type)
                )
            except IntegrityError as exc:
                raise self._error_parser.parse_error(this_animal_type, exc)


class AnimalReader(SQLAlchemyRepo, IAnimalReader, IAnimalVisitedLocationReader):

    def __init__(self, anima_query_builder: BaseQueryBuilder,
                 visited_location: BaseQueryBuilder, **kwargs):
        self.animal_query_builder = anima_query_builder
        self.visited_location_query_builder = visited_location
        super().__init__(**kwargs)

    async def get_animal_by_id(self, animal_id: int) -> AnimalDTO:
        sql = select(AnimalDB).where(AnimalDTO.id == animal_id)
        result = await self._session.execute(sql)
        model = result.scalar()
        if not model:
            raise AnimalNotFound(animal_id)
        return self._mapper.load(AnimalDTO, model)

    async def search_anima(self,
                           start_datetime: datetime,
                           end_datetime: datetime,
                           chipper_id: int,
                           chipping_location_id: int,
                           life_status: LifeStatus,
                           gender: Gender,
                           limit: int,
                           offset: int
                           ) -> List[AnimalDTO]:

        sql = self.animal_query_builder.get_query(start_datetime=start_datetime,
                                                  end_datetime=end_datetime,
                                                  chipper_id=chipper_id,
                                                  chipping_location_id=chipping_location_id,
                                                  life_status=life_status,
                                                  gender=gender,
                                                  offset=offset,
                                                  limit=limit)

        result = await self._session.execute(sql)
        models = result.scalars().all()
        return self._mapper.load(AnimalDB, models)

    async def get_visited_locations(self,
                                    animal_id: int,
                                    start_datetime: datetime,
                                    end_datetime: datetime,
                                    limit: int,
                                    offset: int
                                    ) -> List[AnimalVisitedLocationDTO]:

        check_exist = exists(AnimalDB.id).where(AnimalDB.id == animal_id).select()
        result = await self._session.execute(check_exist)
        check_result = result.scalar()

        if not check_result:
            raise AnimalNotFound(animal_id)

        sql = self.visited_location_query_builder.get_query(start_datetime=start_datetime,
                                                            end_datetime=end_datetime,
                                                            offset=offset,
                                                            limit=limit)

        result = await self._session.execute(sql)
        models = result.scalars().all()
        return self._mapper.load(AnimalVisitedLocationDTO, models)
