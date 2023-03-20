from fastapi import Depends

from src.application.account.dto.account import CreateAccountDTO
from src.application.account.usecases.account import AccountService

from src.presentation.api.presenter.presenter import Presenter
from src.presentation.api.providers.abstract.common import presenter_provider
from src.presentation.api.providers.abstract.services import account_provider_without_auth

from src.presentation.api.handlers.user.registration.requests.post_request import AccountCreateVM
from src.presentation.api.handlers.user.account.responses.account import AccountVM

from src.presentation.api.handlers.user.registration.controllers.router import register_router


@register_router.post('', status_code=201, response_model=AccountVM)
async def registration(
        account_data: AccountCreateVM,
        account_service: AccountService = Depends(account_provider_without_auth),
        presenter: Presenter = Depends(presenter_provider)
) -> AccountVM:
    create_account_dto = CreateAccountDTO(
        first_name=account_data.first_name,
        last_name=account_data.last_name,
        email=account_data.email,
        password=account_data.password
    )
    account_dto = await account_service.create_account(create_account_dto)
    return presenter.load(AccountVM, account_dto)
