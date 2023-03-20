from typing import Any

from fastapi import Depends

from src.application.account.dto.account import AccountDTO
from src.application.account.usecases.account import AccountService
from src.application.account.usecases.auth import AuthService
from src.application.animal.usecases.animal import AnimalService
from src.application.animal.usecases.animal_visited_location import AnimalVisitedLocationService
from src.application.animal.usecases.type_of_specific_animal import TypeOfSpecificAnimalUseCse
from src.application.animal_type.usecases.animal_type import AnimalTypeService
from src.application.location_point.usecases.location_point import LocationPointService

from src.infrastructure.database.uow.uow import UoW
from src.infrastructure.mapper.mapper import Mapper
from src.infrastructure.hasher import Hasher

from src.presentation.api.providers.abstract.common import uow_provider, mapper_provider, hasher_provider
from src.presentation.api.providers.abstract.auth import optional_auth_provider, auth_provider, \
    without_auth_provider


def auth_service_getter(uow: UoW = Depends(uow_provider),
                        mapper: Mapper = Depends(mapper_provider),
                        hasher: Hasher = Depends(hasher_provider)):
    return AuthService(uow=uow, mapper=mapper, hasher=hasher)


def account_service_with_optional_getter(_: Any = Depends(optional_auth_provider),
                                         uow: UoW = Depends(uow_provider),
                                         mapper: Mapper = Depends(mapper_provider)):
    return AccountService(uow=uow, mapper=mapper, hasher=None, current_user=None)


def account_service_without_auth_getter(_: Any = Depends(without_auth_provider),
                                        uow: UoW = Depends(uow_provider),
                                        mapper: Mapper = Depends(mapper_provider),
                                        hasher: Hasher = Depends(hasher_provider)):
    return AccountService(uow=uow, mapper=mapper, hasher=hasher, current_user=None)


def account_service_with_auth_getter(user_dto: AccountDTO = Depends(auth_provider),
                                     uow: UoW = Depends(uow_provider),
                                     mapper: Mapper = Depends(mapper_provider),
                                     hasher: Hasher = Depends(hasher_provider)):
    return AccountService(uow=uow, current_user=user_dto, mapper=mapper, hasher=hasher)


def animal_service_getter(uow: UoW = Depends(uow_provider), mapper: Mapper = Depends(mapper_provider)):
    return AnimalService(uow=uow, mapper=mapper)


def animal_type_service_getter(uow: UoW = Depends(uow_provider), mapper: Mapper = Depends(mapper_provider)):
    return AnimalTypeService(uow=uow, mapper=mapper)


def animal_visited_location_getter(uow: UoW = Depends(uow_provider), mapper: Mapper = Depends(mapper_provider)):
    return AnimalVisitedLocationService(uow=uow, mapper=mapper)


def type_of_specific_getter(uow: UoW = Depends(uow_provider), mapper: Mapper = Depends(mapper_provider)):
    return TypeOfSpecificAnimalUseCse(uow=uow, mapper=mapper)


def location_point_getter(uow: UoW = Depends(uow_provider), mapper: Mapper = Depends(mapper_provider)):
    return LocationPointService(uow=uow, mapper=mapper)
