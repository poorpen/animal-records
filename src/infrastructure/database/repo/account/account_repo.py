from typing import List

from sqlalchemy import insert, select, delete, func
from sqlalchemy.exc import IntegrityError

from src.domain.account.entities.account import Account

from src.application.account.dto.account import AccountDTO
from src.application.account.exceptions.account import AccountNotFoundByID, AccountNotFoundByEmail, AccountHaveAnimal
from src.application.account.interfaces.repo.account_repo import IAccountRepo, IAccountReader

from src.infrastructure.database.repo.common.base_repo import SQLAlchemyRepo
from src.infrastructure.database.models.account import AccountDB


class AccountRepo(SQLAlchemyRepo, IAccountRepo):

    async def add_account(self, account: Account) -> int:
        sql = insert(AccountDB).values(first_name=account.first_name,
                                       last_name=account.last_name,
                                       email=account.email,
                                       password=account.password).returning(AccountDB.id)
        try:
            result = await self._session.execute(sql)
        except IntegrityError as exc:
            raise self._error_parser.parse_error(account, exc)
        row_id = result.scalar()
        return row_id

    async def get_account_by_id(self, account_id: int) -> Account:
        sql = select(AccountDB).where(AccountDB.id == account_id)
        result = await self._session.execute(sql)
        model = result.scalar()
        if not model:
            raise AccountNotFoundByID(account_id)
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
            raise self._error_parser.parse_error(account, exc)

    async def delete_account(self, account_id: int) -> None:
        sql = delete(AccountDB).where(AccountDB.id == account_id).returning(AccountDB.id)
        try:
            result = await self._session.execute(sql)
        except IntegrityError:
            raise AccountHaveAnimal(account_id)
        deleted_row_id = result.scalar()
        if not deleted_row_id:
            raise AccountNotFoundByID(account_id)


class AccountReader(SQLAlchemyRepo, IAccountReader):

    async def get_account_by_id(self, account_id: int) -> AccountDTO:
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
    ) -> List[AccountDTO]:
        sql = self._query_builder.get_query(first_name=first_name,
                                            last_name=last_name,
                                            email=email,
                                            offset=offset,
                                            limit=limit,
                                            )
        print(type(sql))
        result = await self._session.execute(sql)
        models = result.scalars().all()
        return self._mapper.load(AccountDTO, models)
