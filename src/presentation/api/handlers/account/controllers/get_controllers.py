from typing import List

from fastapi import Depends, status

from src.presentation.api.providers.abstract.common import uow_provider, mapper_provider
from src.presentation.api.providers.abstract.services import account_provider
from src.presentation.api.handlers.account.responses.account import AccountsVM
from src.presentation.api.handlers.account.controllers.common import account_router
