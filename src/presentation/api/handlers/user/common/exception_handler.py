from fastapi.responses import JSONResponse

from src.application.account.exceptions import account


def user_exception_handler(_, err: account.AccountIDException):
    match err:
        case account.AccountNotFoundByID():
            return JSONResponse(status_code=404, content={'message': err.message()})
        case (account.AccountAlreadyExist() | account.AccountNotFoundByEmail()):
            return JSONResponse(status_code=409, content={'message': err.message()})
        case account.AccountHaveAnimal():
            return JSONResponse(status_code=400, content={'message': err.message()})
        case account.AccountAccessError():
            return JSONResponse(status_code=403, content={'message': err.message()})

