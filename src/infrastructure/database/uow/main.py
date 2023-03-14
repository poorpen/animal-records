from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.interfaces.mapper import IMapper

from src.infrastructure.database import repo
from src.infrastructure.database.uow.uow import UoW


def build_uow(session: AsyncSession, mapper: IMapper) -> UoW:
    return UoW(
        session=session,
        mapper=mapper,
        account_repo=repo.AccountRepo,
        account_reader=repo.AccountReader,
        animal_repo=repo.AnimalRepo,
        animal_reader=repo.AnimalReader,
        animal_type_repo=repo.AnimalTypeRepo,
        animal_type_reader=repo.AnimalTypeReader,
        location_point_repo=repo.LocationPointRepo,
        location_point_reader=repo.LocationPointReader
    )
