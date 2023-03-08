from abc import ABC

from src.application.common.interfaces.mapper import IMapper

from src.application.account.interfaces.uow.account_uow import IAccountUOW
from src.application.account.dto.auth import AuthAccountDTO
from src.application.account.dto.account import AccountDTO
from src.application.account.exceptions.auth import InvalidEmail, InvalidPassword
from src.application.account.exceptions.account import AccountNotFoundByEmail
from src.application.account.interfaces.hasher.hasher import IHasher


class AuthUseCase(ABC):

    def __init__(self, uow: IAccountUOW, mapper: IMapper, hasher: IHasher):
        self._uow = uow
        self._mapper = mapper
        self._hasher = hasher


class AuthenticateUser(AuthUseCase):

    async def __call__(self, auth_data: AuthAccountDTO) -> AccountDTO:
        try:
            account = await self._uow.account_repo.get_account_by_email(auth_data.email)
        except AccountNotFoundByEmail:
            raise InvalidEmail(auth_data.email)
        if not self._hasher.verify(auth_data.password, account.password):
            raise InvalidPassword()
        return self._mapper.load(AccountDTO, account)


class AuthService:

    def __init__(self, uow: IAccountUOW, mapper: IMapper, hasher: IHasher):
        self._uow = uow
        self._mapper = mapper
        self._hasher = hasher

    async def authenticate_user(self, auth_data: AuthAccountDTO) -> AccountDTO:
        return await AuthenticateUser(self._uow, self._mapper, self._hasher)(auth_data)
