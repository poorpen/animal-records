from typing import List

from fastapi import Depends, Request
from fastapi.responses import JSONResponse

from src.application.account.usecases.account import AccountService

from src.presentation.api.providers.abstract.services import account_provider_with_auth

from src.presentation.api.handlers.user.account.controllers.router import account_router


@account_router.delete('/{account_id}')
async def get_account(
        account_id: int,
        account_service: AccountService = Depends(account_provider_with_auth)
) -> JSONResponse:
    await account_service.delete_account(account_id)
    return JSONResponse(status_code=200, content={'message': "Запрос успешно выполнен"})
