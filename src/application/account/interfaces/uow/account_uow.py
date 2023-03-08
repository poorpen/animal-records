from src.application.common.interfaces.uow.base import IUoW

from src.application.account.interfaces.repo.account_repo import IAccountReader, IAccountRepo


class IAccountUOW(IUoW):
    account_repo: IAccountRepo
    account_reader: IAccountReader
