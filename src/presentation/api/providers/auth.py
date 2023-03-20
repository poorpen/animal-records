from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.application.account.dto.auth import AuthAccountDTO
from src.application.account.usecases.auth import AuthService

from src.presentation.api.providers.abstract.services import auth_service_provider
from src.presentation.api.optional_auth import OptionalAuthorizationBasic

optional_auth = OptionalAuthorizationBasic()
security_auth = HTTPBasic()


async def optional_auth_getter(credentials: HTTPBasicCredentials = Depends(optional_auth),
                               auth_service: AuthService = Depends(auth_service_provider)):
    if credentials:
        auth_dto = AuthAccountDTO(
            email=credentials.username,
            password=credentials.password
        )
        return await auth_service.authenticate_user(auth_dto)


async def auth_getter(credentials: HTTPBasicCredentials = Depends(security_auth),
                      auth_service: AuthService = Depends(auth_service_provider)):
    auth_dto = AuthAccountDTO(
        email=credentials.username,
        password=credentials.password
    )
    return await auth_service.authenticate_user(auth_dto)


async def without_auth_getter(credentials: HTTPBasicCredentials = Depends(optional_auth)):
    if credentials:
        raise HTTPException(status_code=403,
                            detail={'message': "Отправлен запрос регистрации от авторизированного аккаунта"})
