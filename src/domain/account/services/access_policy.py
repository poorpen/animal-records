from src.domain.account.entities.account import Account


class UserAccessPolicy:

    def __init__(self, user: Account):
        self.current_user = user

    def check_self(self, account_id: int) -> bool:
        if self.current_user.id == account_id:
            return True
        return False
