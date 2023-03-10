from sqlalchemy import select, delete, insert, exists
from sqlalchemy.exc import IntegrityError

from src.domain.animal_type.entities.animal_type import AnimalType

from src.application.common.exceptions.application import ApplicationException
from src.application.animal_type.dto.animal_type import AnimalTypeDTO
from src.application.animal_type.exceptions.animal_type import AnimalTypeNotFound, AnimalHaveType, AnimalTypeAlreadyExist
from src.application.animal_type.interfaces.repo.animal_type_repo import IAnimalTypeRepo, IAnimalTypeReader

from src.infrastructure.database.repo.common.base_repo import SQLAlchemyRepo
from src.infrastructure.database.models.animal_type import AnimalTypeDB


class AnimalTypeRepo(SQLAlchemyRepo, IAnimalTypeRepo):

    async def add_type(self, animal_type: AnimalType) -> None:
        sql = insert(AnimalTypeDB).where(type=animal_type.type).returning(AnimalTypeDB.id)
        try:
            result = await self._session.execute(sql)
        except IntegrityError as exc:
            raise self._error_parser(animal_type, exc)
        row_id = result.scalar()
        return row_id

    async def get_type_by_id(self, animal_type_id: int) -> AnimalType:
        sql = select(AnimalTypeDB).where(AnimalTypeDB.id == animal_type_id)
        result = await self._session.execute(sql)
        model = result.scalar()
        if not model:
            AnimalTypeNotFound(animal_type_id)
        return self._mapper.load(AnimalType, model)

    async def change_type(self, animal_type: AnimalType) -> None:
        animal_type_db = self._mapper.load(AnimalTypeDB, animal_type)
        try:
            await self._session.merge(animal_type_db)
        except IntegrityError as exc:
            raise self._error_parser(animal_type, exc)

    async def delete_type(self, animal_type_id: int) -> None:
        sql = delete(AnimalTypeDB).where(AnimalTypeDB.id == animal_type_id).returning(AnimalTypeDB.id)
        try:
            result = await self._session.execute(sql)
        except IntegrityError:
            raise AnimalHaveType(animal_type_id)
        deleted_row_id = result.scalar()
        if not deleted_row_id:
            raise AnimalTypeNotFound(animal_type_id)

    async def check_exist(self, animal_type_id) -> bool:
        sql = exists(AnimalTypeDB.id).where(AnimalTypeDB.id == animal_type_id).select()
        result = await self._session.execute(sql)
        check_result = result.scalar()
        return check_result

    @staticmethod
    def _error_parser(animal_type: AnimalType, exception: IntegrityError) -> ApplicationException:
        database_column = exception.__cause__.__cause__.constraint_name
        if database_column == 'animal_types_type_key':
            return AnimalTypeAlreadyExist(animal_type.type)


class AnimalTypeReader(SQLAlchemyRepo, IAnimalTypeReader):

    async def get_type_by_id(self, animal_type_id: int) -> AnimalTypeDTO:
        sql = select(AnimalTypeDB).where(AnimalTypeDB.id == animal_type_id)
        result = await self._session.execute(sql)
        model = result.scalar()
        if not model:
            raise AnimalTypeNotFound(animal_type_id)
        return self._mapper.load(AnimalTypeDTO, model)
