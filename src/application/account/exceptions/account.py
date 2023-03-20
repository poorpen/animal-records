from dataclasses import dataclass

from src.application.common.exceptions.application import ApplicationException


class BaseAccountException(ApplicationException):
    ...


@dataclass
class AccountAlreadyExist(BaseAccountException):
    email: str

    def message(self):
        return f'Аккаунт с email {self.email} уже существует'


@dataclass
class AccountNotFoundByEmail(BaseAccountException):
    email: str

    def message(self):
        return f'Аккаунт с email {self.email} не найден'


@dataclass
class AccountIDException(BaseAccountException):
    account_id: int


@dataclass
class AccountNotFoundByID(AccountIDException):

    def message(self):
        return f'Аккаунт с account_id {self.account_id} не найден'


@dataclass
class AccountAccessError(AccountIDException):

    def message(self):
        return f'Ошибка доступа к аккаунту с account_id {self.account_id}! ' \
               f'Возможно вы не являетесь владельцем данного аккаунта '


@dataclass
class AccountHaveAnimal(AccountIDException):

    def message(self):
        return f'Аккаунт с account_id {self.account_id} связан с животным'
