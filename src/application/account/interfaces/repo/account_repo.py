from typing import Protocol

from src.domain.account.entities.account import Account

from src.application.account.dto.account import AccountDTO, AccountDTOs


class IAccountRepo(Protocol):

    async def get_account_by_id(self, account_id: int) -> Account:
        raise NotImplementedError

    async def get_account_by_email(self, email: str) -> Account:
        raise NotImplementedError

    async def add_account(self, account: Account) -> int:
        raise NotImplementedError

    async def update_account(self, account: Account) -> None:
        raise NotImplementedError

    async def delete_account(self, account_id: int) -> None:
        raise NotImplementedError


class IAccountReader(Protocol):

    async def get_account_by_id(self, account_id: int) -> AccountDTO:
        raise NotImplementedError

    async def get_accounts(
            self,
            first_name: str,
            last_name: str,
            email: str,
            limit: int,
            offset: int
    ) -> AccountDTOs:
        raise NotImplementedError
