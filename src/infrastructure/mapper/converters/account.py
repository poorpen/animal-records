from typing import List

from src.domain.account.value_objects import FirstName, LastName, Email, AccountID
from src.domain.account.entities.account import Account

from src.application.account.dto.account import AccountDTO, AccountDTOs

from src.infrastructure.database.models.account import AccountDB

from src.infrastructure.mapper.decor import converter


def convert_to_dto(data: Account | AccountDB):
    return AccountDTO(
        id=data.id,
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email
    )


@converter(Account, AccountDTO)
def account_entity_to_dto_converter(data: Account) -> AccountDTO:
    return AccountDTO(
        id=data.id.to_id(),
        first_name=data.first_name.to_string(),
        last_name=data.last_name.to_string(),
        email=data.email.to_string()
    )


@converter(Account, AccountDB)
def account_entity_to_model_converter(data: Account) -> AccountDB:
    return AccountDB(
        id=data.id.to_id(),
        first_name=data.first_name.to_string(),
        last_name=data.last_name.to_string(),
        email=data.email.to_string(),
        password=data.password
    )


@converter(AccountDTO, Account)
def account_dto_to_entity_converter(data: AccountDTO) -> Account:
    return Account(
        id=AccountID(data.id),
        first_name=FirstName(data.first_name),
        last_name=LastName(data.last_name),
        email=Email(data.email),
        password=None
    )


@converter(AccountDB, Account)
def account_model_to_entity_converter(data: AccountDB) -> Account:
    return Account(
        id=AccountID(data.id),
        first_name=FirstName(data.first_name),
        last_name=LastName(data.last_name),
        email=Email(data.email),
        password=data.password
    )


@converter(AccountDB, AccountDTO)
def account_model_to_dto_converter(data: AccountDB) -> AccountDTO:
    return convert_to_dto(data)


@converter(list, AccountDTOs)
def account_models_to_dtos_converter(data: List[AccountDB]) -> AccountDTOs:
    return AccountDTOs(accounts=[
        convert_to_dto(account_db) for account_db in data
    ])
