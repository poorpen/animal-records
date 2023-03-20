from src.domain.account.entities.account import Account
from src.domain.account.value_objects import AccountID


class UserAccessPolicy:

    def __init__(self, user: Account):
        self.current_user = user

    def check_self(self, account_id: int) -> bool:
        current_id = AccountID(account_id)
        if self.current_user.id == current_id:
            return True
        return False
