from abc import ABC

from src.domain.account.value_objects import AccountID, FirstName, LastName, Email, Password
from src.domain.account.entities.account import Account
from src.domain.account.services.access_policy import UserAccessPolicy

from src.application.common.interfaces.mapper import IMapper

from src.application.account.interfaces.hasher.hasher import IHasher
from src.application.account.interfaces.uow.account_uow import IAccountUOW
from src.application.account.dto.account import AccountDTO, SearchParametersDTO, CreateAccountDTO, UpdateAccountDTO, \
    AccountDTOs
from src.application.account.exceptions.account import AccountAlreadyExist, AccountAccessError, AccountHaveAnimal


class AccountUseCase(ABC):

    def __init__(self, uow: IAccountUOW, mapper: IMapper, hasher: IHasher):
        self._uow = uow
        self._mapper = mapper
        self._hasher = hasher


class CreateAccount(AccountUseCase):

    async def __call__(self, create_account_dto: CreateAccountDTO) -> AccountDTO:
        hashed_password = self._hasher.hash(Password(create_account_dto.password).to_string())
        account = Account.create(
            email=Email(create_account_dto.email),
            first_name=FirstName(create_account_dto.first_name),
            last_name=LastName(create_account_dto.last_name),
            password=hashed_password
        )
        try:
            account_id = await self._uow.account_repo.add_account(account)
            await self._uow.commit()
        except AccountAlreadyExist:
            await self._uow.rollback()
            raise
        account.update(account_id=AccountID(account_id))
        return self._mapper.load(AccountDTO, account)


class UpdateAccount(AccountUseCase):

    async def __call__(self, account_dto: UpdateAccountDTO) -> AccountDTO:
        hashed_password = self._hasher.hash(Password(account_dto.password).to_string())
        account = await self._uow.account_repo.get_account_by_id(account_id=AccountID(account_dto.id))
        account.update(
            first_name=FirstName(account_dto.first_name),
            last_name=LastName(account_dto.last_name),
            email=Email(account_dto.email),
            password=hashed_password
        )
        try:
            await self._uow.account_repo.update_account(account)
            await self._uow.commit()
        except AccountAlreadyExist:
            await self._uow.rollback()
            raise
        return self._mapper.load(AccountDTO, account)


class GetAccount(AccountUseCase):

    async def __call__(self, account_id: int) -> AccountDTO:
        return await self._uow.account_reader.get_account_by_id(account_id=account_id)


class SearchAccounts(AccountUseCase):

    async def __call__(self, search_parameters_dto: SearchParametersDTO) -> AccountDTOs:
        return await self._uow.account_reader.get_accounts(
            first_name=search_parameters_dto.first_name,
            last_name=search_parameters_dto.last_name,
            email=search_parameters_dto.email,
            limit=search_parameters_dto.limit,
            offset=search_parameters_dto.offset

        )


class DeleteAccount(AccountUseCase):

    async def __call__(self, account_id: int) -> None:
        try:
            await self._uow.account_repo.delete_account(account_id=AccountID(account_id))
            await self._uow.commit()
        except AccountHaveAnimal:
            await self._uow.rollback()
            raise


class AccountService:

    def __init__(self, uow: IAccountUOW, mapper: IMapper, hasher: IHasher, current_user: AccountDTO | None):
        self._uow = uow
        self._mapper = mapper
        self._hasher = hasher
        self._access_policy = UserAccessPolicy(mapper.load(Account, current_user))

    async def create_account(self, account_dto: CreateAccountDTO) -> AccountDTO:
        return await CreateAccount(self._uow, self._mapper, self._hasher)(account_dto)

    async def update_account(self, account_dto: UpdateAccountDTO) -> AccountDTO:
        if not self._access_policy.check_self(account_dto.id):
            raise AccountAccessError(account_dto.id)
        return await UpdateAccount(self._uow, self._mapper, self._hasher)(account_dto)

    async def get_account(self, account_id: int) -> AccountDTO:
        return await GetAccount(self._uow, self._mapper, self._hasher)(account_id)

    async def search_accounts(self, search_parameters_dto: SearchParametersDTO) -> AccountDTOs:
        return await SearchAccounts(self._uow, self._mapper, self._hasher)(search_parameters_dto)

    async def delete_account(self, account_id: int) -> None:
        if not self._access_policy.check_self(account_id):
            raise AccountAccessError(account_id)
        await DeleteAccount(self._uow, self._mapper, self._hasher)(account_id)
