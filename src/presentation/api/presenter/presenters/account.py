from src.application.account.dto.account import AccountDTO, AccountDTOs

from src.infrastructure.mapper.decor import converter

from src.presentation.api.handlers.user.account.responses.account import AccountVM, AccountsVM


def dto_to_vm(data: AccountDTO) -> AccountVM:
    return AccountVM(
        id=data.id,
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        by_alies=True
    )


@converter(AccountDTO, AccountVM)
def convert_dto_to_vm(data: AccountDTO) -> AccountVM:
    return dto_to_vm(data)


@converter(AccountDTOs, AccountsVM)
def convert_dtos_to_vms(data: AccountDTOs) -> AccountsVM:
    return AccountsVM(accounts=[dto_to_vm(account) for account in data.accounts])
