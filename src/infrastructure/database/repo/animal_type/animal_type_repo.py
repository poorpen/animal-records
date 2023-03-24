from sqlalchemy import select, delete, insert, exists, update
from sqlalchemy.exc import IntegrityError

from src.domain.animal_type.entities.animal_type import AnimalType

from src.application.common.exceptions.application import ApplicationException
from src.application.animal_type.dto.animal_type import AnimalTypeDTO
from src.application.animal_type.exceptions.animal_type import AnimalTypeNotFound, AnimalHaveType, \
    AnimalTypeAlreadyExist
from src.application.animal_type.interfaces.repo.animal_type_repo import IAnimalTypeRepo, IAnimalTypeReader
from src.domain.animal_type.value_objects import AnimalTypeID

from src.infrastructure.database.repo.common.base_repo import SQLAlchemyRepo
from src.infrastructure.database.models.animal_type import AnimalTypeDB


class AnimalTypeRepo(SQLAlchemyRepo, IAnimalTypeRepo):

    async def add_type(self, animal_type: AnimalType) -> None:
        sql = insert(AnimalTypeDB).values(type=animal_type.type.to_string()).returning(AnimalTypeDB.id)
        try:
            result = await self._session.execute(sql)
        except IntegrityError as exc:
            raise self._error_parser(animal_type, exc)
        row_id = result.scalar()
        return row_id

    async def get_type_by_id(self, animal_type_id: AnimalTypeID) -> AnimalType:
        sql = select(AnimalTypeDB).where(AnimalTypeDB.id == animal_type_id.to_id())
        result = await self._session.execute(sql)
        model = result.scalar()
        if not model:
            raise AnimalTypeNotFound(animal_type_id.to_id())
        return self._mapper.load(AnimalType, model)

    async def change_type(self, animal_type: AnimalType) -> None:
        type_db = self._mapper.load(AnimalTypeDB, animal_type)
        try:
            await self._session.merge(type_db)
            await self._session.flush()
        except IntegrityError as exc:
            raise self._error_parser(animal_type, exc)

    async def delete_type(self, animal_type_id: AnimalTypeID) -> None:
        sql = delete(AnimalTypeDB).where(AnimalTypeDB.id == animal_type_id.to_id()).returning(AnimalTypeDB.id)
        try:
            result = await self._session.execute(sql)
        except IntegrityError:
            raise AnimalHaveType(animal_type_id.to_id())
        deleted_row_id = result.scalar()
        if not deleted_row_id:
            raise AnimalTypeNotFound(animal_type_id.to_id())

    @staticmethod
    def _error_parser(animal_type: AnimalType, exception: IntegrityError) -> ApplicationException:
        database_column = exception.__cause__.__cause__.constraint_name
        if database_column == 'animal_types_type_key':
            return AnimalTypeAlreadyExist(animal_type.type.to_string())


class AnimalTypeReader(SQLAlchemyRepo, IAnimalTypeReader):

    async def get_type_by_id(self, animal_type_id: int) -> AnimalTypeDTO:
        self._validate_id(animal_type_id, 'animal_type_id')
        sql = select(AnimalTypeDB).where(AnimalTypeDB.id == animal_type_id)
        result = await self._session.execute(sql)
        model = result.scalar()
        if not model:
            raise AnimalTypeNotFound(animal_type_id)
        return self._mapper.load(AnimalTypeDTO, model)
