from fastapi.responses import JSONResponse

from src.application.animal_type.exceptions import animal_type


def animal_type_exception_handler(_, err: animal_type.BaseAnimalTypeException):
    match err:
        case animal_type.AnimalTypeNotFound():
            return JSONResponse(status_code=404, content={'message': err.message()})
        case animal_type.AnimalTypeAlreadyExist():
            return JSONResponse(status_code=409, content={'message': err.message()})
        case animal_type.AnimalHaveType():
            return JSONResponse(status_code=400, content={'message': err.message()})
