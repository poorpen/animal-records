import pytest

from src.domain.account.entities.account import Account
from src.application.account.dto.account import AccountDTO, AccountDTOs
from src.infrastructure.database.models.account import AccountDB

from test.test_infrastructure.test_mapper.common import mapper


@pytest.fixture
def account_entity():
    return Account(id=1, first_name='first_name', last_name='last_name', email='example@localhost.com',
                   password='password')


@pytest.fixture
def account_db_model():
    model = AccountDB(id=1, first_name='first_name', last_name='last_name', email='example@localhost.com',
                     password='password')
    model.__dict__.pop('_sa_instance_state')
    return model


@pytest.fixture
def account_dto():
    return AccountDTO(id=1, first_name='first_name', last_name='last_name', email='example@localhost.com')


def test_entity_to_dto(mapper, account_entity, account_dto):
    result = mapper.load(AccountDTO, account_entity)
    assert result == account_dto


def test_entity_to_model(mapper, account_entity, account_db_model):
    result = mapper.load(AccountDB, account_entity)
    result.__dict__.pop('_sa_instance_state')
    assert result.__dict__ == account_db_model.__dict__
    assert type(result) == type(account_db_model)


def test_model_to_entity(mapper, account_db_model, account_entity):
    result = mapper.load(Account, account_db_model)
    assert result == account_entity


def test_model_to_dto(mapper, account_db_model, account_dto):
    result = mapper.load(AccountDTO, account_db_model)
    assert result == account_dto


def test_models_to_dtos(mapper, account_db_model, account_dto):
    expected_res = AccountDTOs(accounts=[account_dto, account_dto, account_dto])
    result = mapper.load(AccountDTOs, [account_db_model, account_db_model, account_db_model])
    assert result == expected_res
