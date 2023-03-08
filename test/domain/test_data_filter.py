import pytest

from typing import Dict, Any

from src.domain.common.constants.empty import Empty
from src.domain.common.utils.data_filter import data_filter


@pytest.fixture
def data():
    data: Dict[str, Any] = {'string': 'test_text', 'integer': 69, 'bool': True}
    return data


def test_when_value_is_empty(data):
    data['string'] = Empty.UNSET
    result = data_filter(**data)
    expected_data = data
    expected_data.pop('string')
    assert result == expected_data


def test_when_value_is_none(data):
    data['string'] = None
    result = data_filter(**data)
    expected_data = data
    expected_data.pop('string')
    assert result == expected_data


def test_all_data_empty(data):
    data['string'] = Empty.UNSET
    data['integer'] = Empty.UNSET
    data['bool'] = Empty.UNSET
    assert {} == data_filter(**data)


def test_all_data_is_none(data):
    data['string'] = None
    data['integer'] = None
    data['bool'] = None
    assert {} == data_filter(**data)
