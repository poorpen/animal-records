from typing import List

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
    return convert_to_dto(data)


@converter(Account, AccountDB)
def account_entity_to_model_converter(data: Account) -> AccountDB:
    return AccountDB(
        id=data.id,
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        password=data.password
    )


@converter(AccountDB, Account)
def account_model_to_entity_converter(data: AccountDB) -> Account:
    return Account(
        id=data.id,
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
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
