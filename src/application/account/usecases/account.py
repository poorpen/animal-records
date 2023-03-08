from abc import ABC
from typing import List

from src.domain.account.entities.account import Account
from src.domain.account.services.access_policy import UserAccessPolicy

from src.application.common.interfaces.mapper import IMapper

from src.application.account.interfaces.hasher.hasher import IHasher
from src.application.account.interfaces.uow.account_uow import IAccountUOW
from src.application.account.dto.account import AccountDTO, SearchParametersDTO, CreateAccountDTO, UpdateAccountDTO
from src.application.account.exceptions.account import AccountAlreadyExist, AccountNotFoundByID, AccountAccessError


class AccountUseCase(ABC):

    def __init__(self, uow: IAccountUOW, mapper: IMapper, hasher: IHasher):
        self._uow = uow
        self._mapper = mapper
        self._hasher = hasher


class CreateAccount(AccountUseCase):

    async def __call__(self, create_account_dto: CreateAccountDTO) -> AccountDTO:
        hashed_password = self._hasher.hash(create_account_dto.password)
        account = Account.create(
            email=create_account_dto.email,
            first_name=create_account_dto.first_name,
            last_name=create_account_dto.last_name,
            password=hashed_password
        )
        try:
            account_id = await self._uow.account_repo.add_account(account)
            await self._uow.commit()
        except AccountAlreadyExist:
            await self._uow.rollback()
            raise
        account.id = account_id
        return self._mapper.load(AccountDTO, account)


class UpdateAccount(AccountUseCase):

    async def __call__(self, account_dto: UpdateAccountDTO) -> AccountDTO:
        hashed_password = self._hasher.hash(account_dto.password)
        account = await self._uow.account_repo.get_account_by_id(account_id=account_dto.id)
        account.update(
            first_name=account_dto.first_name,
            last_name=account_dto.last_name,
            email=account_dto.email,
            password=hashed_password
        )
        try:
            await self._uow.account_repo.update_account(account)
            await self._uow.commit()
        except (AccountAlreadyExist, AccountNotFoundByID):
            await self._uow.rollback()
            raise
        return self._mapper.load(AccountDTO, account)


class GetAccount(AccountUseCase):

    async def __call__(self, account_id: int) -> AccountDTO:
        return await self._uow.account_reader.get_account_by_id(account_id=account_id)


class SearchAccounts(AccountUseCase):

    async def __call__(self, search_parameters_dto: SearchParametersDTO) -> List[AccountDTO]:
        return await self._uow.account_reader.get_accounts(
            first_name=search_parameters_dto.first_name,
            last_name=search_parameters_dto.last_name,
            email=search_parameters_dto.email,
            limit=search_parameters_dto.limit,
            offset=search_parameters_dto.offset

        )


class DeleteAccount(AccountUseCase):

    async def __call__(self, account_id: int) -> None:
        await self._uow.account_repo.delete_account(account_id=account_id)


class AccountService:

    def __init__(self, uow: IAccountUOW, mapper: IMapper, hasher: IHasher, access_policy: UserAccessPolicy):
        self._uow = uow
        self._mapper = mapper
        self._hasher = hasher
        self._access_policy = access_policy

    async def create_account(self, account_dto: CreateAccountDTO) -> AccountDTO:
        return await CreateAccount(self._uow, self._mapper, self._hasher)(account_dto)

    async def update_account(self, account_dto: UpdateAccountDTO) -> AccountDTO:
        if not self._access_policy.check_self(account_dto.id):
            raise AccountAccessError(account_dto.id)
        return await UpdateAccount(self._uow, self._mapper, self._hasher)(account_dto)

    async def get_account(self, account_id: int) -> AccountDTO:
        return await GetAccount(self._uow, self._mapper, self._hasher)(account_id)

    async def search_accounts(self, search_parameters_dto: SearchParametersDTO) -> List[AccountDTO]:
        return await SearchAccounts(self._uow, self._mapper, self._hasher)(search_parameters_dto)

    async def delete_account(self, account_id: int) -> None:
        if not self._access_policy.check_self(account_id):
            raise AccountAccessError(account_id)
        await DeleteAccount(self._uow, self._mapper, self._hasher)(account_id)
