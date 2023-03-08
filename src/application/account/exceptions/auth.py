from dataclasses import dataclass

from src.application.common.exceptions.application import ApplicationException


@dataclass
class InvalidEmail(ApplicationException):
    email: str

    def message(self):
        return f'Пользователь с таким email {self.email} не зарегистрирован'


class InvalidPassword(ApplicationException):

    def message(self):
        return 'В указанном вами пароле допущена ошибка'
