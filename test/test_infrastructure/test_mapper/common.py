import pytest

from src.infrastructure.mapper.main import build_mapper


@pytest.fixture()
def mapper():
    return build_mapper()
