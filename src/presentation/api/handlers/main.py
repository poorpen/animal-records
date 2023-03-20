from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from src.application.account.exceptions.auth import AuthException
from src.domain.common.exceptions.validation import BaseModelException
from src.domain.animal.exceptions.common import BaseAnimalDomainException

from src.application.account.exceptions.account import BaseAccountException
from src.application.animal.exceptions.common import BaseAnimalException
from src.application.animal_type.exceptions.animal_type import BaseAnimalTypeException
from src.application.location_point.exceptions.location_point import BaseLocationPointException

from src.infrastructure.database.repo.common.exceptions.base import BaseRepoException


from src.presentation.api.handlers.common import common_validation_exception_handler, validation_exception_handler, \
    auth_exception_handler

from src.presentation.api.handlers.user import account_router, register_router, user_exception_handler
from src.presentation.api.handlers.animal import animals_router, animal_exception_handler
from src.presentation.api.handlers.animal_type import animal_type_router, animal_type_exception_handler
from src.presentation.api.handlers.location_point import location_point_router, location_point_exception_handler


def bind_exception_handlers(app: FastAPI):
    app.add_exception_handler(AuthException, auth_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(BaseRepoException, common_validation_exception_handler)
    app.add_exception_handler(BaseModelException, common_validation_exception_handler)
    app.add_exception_handler(BaseAnimalException, animal_exception_handler)
    app.add_exception_handler(BaseAnimalDomainException, animal_exception_handler)
    app.add_exception_handler(BaseAnimalTypeException, animal_type_exception_handler)
    app.add_exception_handler(BaseLocationPointException, location_point_exception_handler)
    app.add_exception_handler(BaseAccountException, user_exception_handler)


def bind_routers(app: FastAPI):
    app.include_router(register_router)
    app.include_router(account_router)
    app.include_router(animals_router)
    app.include_router(animal_type_router)
    app.include_router(location_point_router)
