from typing import List

from sqlalchemy import insert, select, delete
from sqlalchemy.exc import IntegrityError

from src.domain.account.entities.account import Account

from src.application.account.dto.account import AccountDTO, AccountDTOs
from src.application.common.exceptions.application import ApplicationException
from src.application.account.exceptions.account import AccountNotFoundByID, AccountNotFoundByEmail, AccountHaveAnimal, \
    AccountAlreadyExist
from src.application.account.interfaces.repo.account_repo import IAccountRepo, IAccountReader
from src.domain.account.value_objects import AccountID, Email

from src.infrastructure.database.repo.common.base_repo import SQLAlchemyRepo
from src.infrastructure.database.models.account import AccountDB
from src.infrastructure.database.repo.account.account_query_builder import GetAccountQuery


class AccountRepo(SQLAlchemyRepo, IAccountRepo):

    async def add_account(self, account: Account) -> int:
        sql = insert(AccountDB).values(first_name=account.first_name.to_string(),
                                       last_name=account.last_name.to_string(),
                                       email=account.email.to_string(),
                                       password=account.password).returning(AccountDB.id)
        try:
            result = await self._session.execute(sql)
        except IntegrityError as exc:
            raise self._error_parser(account, exc)
        row_id = result.scalar()
        return row_id

    async def get_account_by_id(self, account_id: AccountID) -> Account:
        sql = select(AccountDB).where(AccountDB.id == account_id.to_id())
        result = await self._session.execute(sql)
        model = result.scalar()
        if not model:
            raise AccountNotFoundByID(account_id.to_id())
        return self._mapper.load(Account, model)

    async def get_account_by_email(self, email: str) -> Account:
        sql = select(AccountDB).where(AccountDB.email == email)
        result = await self._session.execute(sql)
        model = result.scalar()
        if not model:
            raise AccountNotFoundByEmail(email)
        return self._mapper.load(Account, model)

    async def update_account(self, account: Account) -> None:
        account_db = self._mapper.load(AccountDB, account)
        try:
            await self._session.merge(account_db)
        except IntegrityError as exc:
            self._error_parser(account, exc)

    async def delete_account(self, account_id: AccountID) -> None:
        sql = delete(AccountDB).where(AccountDB.id == account_id.to_id()).returning(AccountDB.id)
        try:
            result = await self._session.execute(sql)
        except IntegrityError:
            raise AccountHaveAnimal(account_id.to_id())
        deleted_row_id = result.scalar()
        if not deleted_row_id:
            raise AccountNotFoundByID(account_id.to_id())

    @staticmethod
    def _error_parser(account: Account, exception: IntegrityError) -> ApplicationException:
        database_column = exception.__cause__.__cause__.constraint_name
        if database_column == 'accounts_email_key':
            return AccountAlreadyExist(account.email.to_string())


class AccountReader(SQLAlchemyRepo, IAccountReader):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._query_builder = GetAccountQuery()

    async def get_account_by_id(self, account_id: int) -> AccountDTO:
        self._validate_id(account_id, 'account_id')
        sql = select(AccountDB).where(AccountDB.id == account_id)
        result = await self._session.execute(sql)
        model = result.scalar()
        if not model:
            raise AccountNotFoundByID(account_id)
        return self._mapper.load(AccountDTO, model)

    async def get_accounts(
            self,
            first_name: str,
            last_name: str,
            email: str,
            limit: int,
            offset: int
    ) -> AccountDTOs:
        self._validate_limit_offset(limit, offset)
        sql = self._query_builder.get_query(first_name=first_name,
                                            last_name=last_name,
                                            email=email,
                                            offset=offset,
                                            limit=limit,
                                            )
        result = await self._session.execute(sql)
        models = result.scalars().all()
        return self._mapper.load(AccountDTOs, models)
