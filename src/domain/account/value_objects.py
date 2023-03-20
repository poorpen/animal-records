from dataclasses import dataclass
from email_validator import validate_email, EmailNotValidError

from src.domain.common.value_objects.base import ValueObject

from src.domain.common.value_objects.id import IDVO
from src.domain.common.value_objects.text import TextVO

from src.domain.common.exceptions.validation import EmailValidationError


@dataclass
class Email(ValueObject):
    __field_name__ = 'email'
    value: str

    def __post_init__(self):
        try:
            validate_email(self.value)
        except EmailNotValidError:
            raise EmailValidationError(field=self.__field_name__, email=self.value)

    def to_string(self):
        return self.value


class AccountID(IDVO):
    __field_name__ = 'account_id'


class FirstName(TextVO):
    __field_name__ = 'first_name'


class LastName(TextVO):
    __field_name__ = 'last_name'


class Password(TextVO):
    __field_name__ = 'password'
