from fastapi.responses import JSONResponse

from src.application.location_point.exceptions import location_point


def location_point_exception_handler(_, err: location_point.BaseLocationPointException):
    match err:
        case location_point.PointNotFound():
            return JSONResponse(status_code=404, content={'message': err.message()})
        case location_point.PointAlreadyExist():
            return JSONResponse(status_code=409, content={'message': err.message()})
        case location_point.AnimalAssociatedWithPoint():
            return JSONResponse(status_code=400, content={'message': err.message()})
