from typing import List

from fastapi import Depends, Request

from src.application.account.dto.account import SearchParametersDTO
from src.application.account.usecases.account import AccountService

from src.presentation.api.presenter.presenter import Presenter
from src.presentation.api.providers.abstract.common import presenter_provider
from src.presentation.api.providers.abstract.services import account_provider_with_optional_auth

from src.presentation.api.handlers.user.account.requests.get_request import SearchAccountParametersVM
from src.presentation.api.handlers.user.account.responses.account import AccountsVM
from src.presentation.api.handlers.user.account.responses.account import AccountVM
from src.presentation.api.handlers.user.account.controllers.router import account_router

from src.presentation.api.handlers.common.utils.from_getter import from_getter


# @account_router.get('//')
# async def account_id_empty():
#     return JSONResponse(status_code=400, content={'message': 'accountID не был указан'})


@account_router.get('/search')
async def search_accounts(
        request: Request,
        search_parameters: SearchAccountParametersVM = Depends(),
        presenter: Presenter = Depends(presenter_provider),
        account_service: AccountService = Depends(account_provider_with_optional_auth)
) -> List[AccountVM]:
    from_getter(request=request, model=search_parameters)
    search_parameters_dto = SearchParametersDTO(
        first_name=search_parameters.first_name,
        last_name=search_parameters.last_name,
        email=search_parameters.email,
        limit=search_parameters.limit,
        offset=search_parameters.offset
    )
    accounts_dto = await account_service.search_accounts(search_parameters_dto)
    return presenter.load(AccountsVM, accounts_dto).accounts


@account_router.get('/{account_id}', response_model=AccountVM)
async def get_account(
        account_id: int,
        presenter: Presenter = Depends(presenter_provider),
        account_service: AccountService = Depends(account_provider_with_optional_auth)
) -> AccountVM:
    account_dto = await account_service.get_account(account_id)
    return presenter.load(AccountVM, account_dto)
