from typing import List

from src.domain.account.entities.account import Account

from src.application.account.dto.account import AccountDTO

from src.infrastructure.database.models.account import AccountDB


def account_entity_to_dto(data: Account) -> AccountDTO:
    return AccountDTO(
        id=data.id,
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email
    )


def account_entity_to_model(data: Account) -> AccountDB:
    return AccountDB(
        id=data.id,
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        password=data.password
    )


def account_model_to_entity(data: AccountDB) -> Account:
    return Account(
        id=data.id,
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        password=data.password
    )


def account_model_to_dto(data: AccountDB) -> AccountDTO:
    return AccountDTO(
        id=data.id,
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
    )


def account_models_to_dtos(data: List[AccountDB]) -> List[AccountDTO]:
    return [
        account_model_to_dto(account_db) for account_db in data
    ]
