from fastapi import Depends

from src.application.account.dto.account import UpdateAccountDTO
from src.application.account.usecases.account import AccountService

from src.presentation.api.presenter.presenter import Presenter
from src.presentation.api.providers.abstract.common import presenter_provider
from src.presentation.api.providers.abstract.services import account_provider_with_auth

from src.presentation.api.handlers.user.account.requests.put_request import UpdateAccountVM
from src.presentation.api.handlers.user.account.responses.account import AccountVM

from src.presentation.api.handlers.user.account.controllers.router import account_router


@account_router.put('/{account_id}', response_model=AccountVM)
async def registration(
        account_id: int,
        account_data: UpdateAccountVM,
        account_service: AccountService = Depends(account_provider_with_auth),
        presenter: Presenter = Depends(presenter_provider)
) -> AccountVM:
    update_account_dto = UpdateAccountDTO(
        id=account_id,
        first_name=account_data.first_name,
        last_name=account_data.last_name,
        email=account_data.email,
        password=account_data.password
    )
    account_dto = await account_service.update_account(update_account_dto)
    return presenter.load(AccountVM, account_dto)
