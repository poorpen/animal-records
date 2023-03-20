import json

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.application.account.exceptions.auth import AuthException
from src.domain.common.exceptions.validation import BaseModelException

from src.infrastructure.database.repo.common.exceptions.base import BaseRepoException


async def common_validation_exception_handler(_, err: BaseModelException | BaseRepoException):
    return JSONResponse(status_code=400, content={'message': err.message()})


async def auth_exception_handler(_, err: AuthException):
    return JSONResponse(status_code=401, content={'message': err.message()})


async def validation_exception_handler(_, err: ValidationError | RequestValidationError):
    return JSONResponse(
        status_code=400, content=json.loads(err.json()))
