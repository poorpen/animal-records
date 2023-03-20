from typing import Any

from fastapi import Depends

from fastapi.responses import JSONResponse

from src.application.location_point.usecases.location_point import LocationPointService

from src.presentation.api.providers.abstract.auth import auth_provider
from src.presentation.api.providers.abstract.services import location_point_provider

from src.presentation.api.handlers.location_point.controllers.common.router import location_point_router


@location_point_router.delete('/{point_id}')
async def delete_location_point(
        point_id: int,
        location_point_service: LocationPointService = Depends(location_point_provider),
        _: Any = Depends(auth_provider)
) -> JSONResponse:
    await location_point_service.delete_location_point(point_id)
    return JSONResponse(status_code=200, content={'message': "Запрос успешно выполнен"})
