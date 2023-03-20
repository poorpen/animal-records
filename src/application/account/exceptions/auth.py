from dataclasses import dataclass

from src.application.common.exceptions.application import ApplicationException


class AuthException(ApplicationException):
    ...


@dataclass
class InvalidEmail(AuthException):
    email: str

    def message(self):
        return f'Пользователь с таким email {self.email} не зарегистрирован'


class InvalidPassword(AuthException):

    def message(self):
        return 'В указанном вами пароле допущена ошибка'
