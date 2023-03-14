from fastapi import Depends

from src.application.account.usecases.auth import AuthService
from src.application.account.usecases.account import AccountService
from src.application.animal.usecases.animal import AnimalService
from src.application.animal.usecases.animal_visited_location import AnimalVisitedLocationService
from src.application.animal.usecases.type_of_specific_animal import TypeOfSpecificAnimalUseCse
from src.application.animal_type.usecases.animal_type import AnimalTypeService
from src.application.location_point.usecases.location_point import LocationPoint

from src.infrastructure.database.uow.uow import UoW
from src.infrastructure.mapper.mapper import Mapper

from src.presentation.api.providers.abstract.common import uow_provider, mapper_provider


def account_service_getter(uow: UoW = Depends(uow_provider), mapper: Mapper = Depends(mapper_provider)):
    return AccountService(uow=uow, mapper=mapper, hasher=None, current_user=None)


def animal_service_getter(uow: UoW = Depends(uow_provider), mapper: Mapper = Depends(mapper_provider)):
    return AnimalService(uow=uow, mapper=mapper)


def animal_type_service_getter(uow: UoW = Depends(uow_provider), mapper: Mapper = Depends(mapper_provider)):
    return AnimalTypeService(uow=uow, mapper=mapper)


def animal_visited_location_getter(uow: UoW = Depends(uow_provider), mapper: Mapper = Depends(mapper_provider)):
    return AnimalVisitedLocationService(uow=uow, mapper=mapper)
