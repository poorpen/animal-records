from src.domain.account.entities.account import Account

from src.application.account.exceptions.account import AccountAlreadyExist


def account_already_exist_with_this_email(account: Account):
    return AccountAlreadyExist(account.email)
