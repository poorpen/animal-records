from src.application.common.exceptions.application import ApplicationException


class InvalidID(ApplicationException):
    field_name: str

    def message(self):
        return f'Ошибка валидации: переданный вами {self.field_name} <= 0'
