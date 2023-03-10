from typing import Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.interfaces.mapper import IMapper

from src.application.account.interfaces.repo import IAccountRepo, IAccountReader
from src.application.animal_type.interfaces.repo import IAnimalTypeRepo, IAnimalTypeReader
from src.application.location_point.interfaces.repo import ILocationPointRepo, ILocationPointReader
from src.application.animal.interfaces.repo import IAnimalRepo, IAnimalReader

from src.infrastructure.database.uow.base import BaseUoW


class UoW(BaseUoW):
    account_repo: IAccountRepo
    account_reader: IAccountReader
    animal_repo: IAnimalRepo
    animal_reader: IAnimalReader
    animal_type_repo: IAnimalTypeRepo
    animal_type_reader: IAnimalTypeReader
    location_point_repo: ILocationPointRepo
    location_point_reader: ILocationPointReader

    def __init__(self,
                 session: AsyncSession,
                 mapper: IMapper,

                 account_repo: Type[IAccountRepo],
                 account_reader: Type[IAccountReader],
                 animal_repo: Type[IAnimalRepo],
                 animal_reader: Type[IAnimalReader],
                 animal_type_repo: Type[IAnimalTypeRepo],
                 location_point_repo: Type[ILocationPointRepo],
                 location_point_reader: Type[ILocationPointReader]
                 ):
        super().__init__(session=session)
        self.account_repo = account_repo(session=session, mapper=mapper)
        self.account_reader = account_reader(session=session, mapper=mapper)
        self.animal_repo = animal_repo(session=session, mapper=mapper)
        self.animal_reader = animal_reader(session=session, mapper=mapper)
        self.animal_type_repo = animal_type_repo(session=session, mapper=mapper)
        self.location_point_repo = location_point_repo(session=session, mapper=mapper)
        self.location_point_reader = location_point_reader(session=session, mapper=mapper)
