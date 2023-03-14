from email_validator import validate_email, EmailNotValidError

from src.domain.common.exceptions.validation import EmptyField, EmailValidationError, EnumError


def text_field_validation(field_name, v):
    if not v or v.isspace():
        raise EmptyField(field=field_name)


def email_validation(field_name, v):
    try:
        validate_email(v)
    except EmailNotValidError:
        raise EmailValidationError(field=field_name, email=v)


def enum_validation(field_name, v, enum):
    try:
        enum(v)
    except ValueError:
        raise EnumError(field_name, v, list(map(lambda enum_attr: enum_attr.value, enum)))
