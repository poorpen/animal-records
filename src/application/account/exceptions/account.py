from dataclasses import dataclass

from src.application.common.exceptions.application import ApplicationException


@dataclass
class AccountAlreadyExist(ApplicationException):
    email: str

    def message(self):
        return f'Аккаунт с email {self.email} уже существует'


@dataclass
class AccountNotFoundByEmail(ApplicationException):
    email: str

    def message(self):
        return f'Аккаунт с email {self.email} не найден'


@dataclass
class BaseAccountException(ApplicationException):
    account_id: int


class AccountNotFoundByID(BaseAccountException):

    def message(self):
        return f'Аккаунт с account_id {self.account_id} не найден'


class AccountAccessError(BaseAccountException):

    def message(self):
        return f'Ошибка доступа к аккаунту с account_id {self.account_id}! ' \
               f'Возможно вы не являетесь владельцем данного аккаунта '


class AccountHaveAnimal(BaseAccountException):

    def message(self):
        return f'Аккаунт с account_id {self.account_id} связан с животным'
