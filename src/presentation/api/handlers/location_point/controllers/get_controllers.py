from typing import Any

from fastapi import Depends

from fastapi.responses import JSONResponse

from src.application.location_point.usecases.location_point import LocationPointService

from src.presentation.api.presenter.presenter import Presenter
from src.presentation.api.providers.abstract.auth import optional_auth_provider
from src.presentation.api.providers.abstract.common import presenter_provider
from src.presentation.api.providers.abstract.services import location_point_provider

from src.presentation.api.handlers.location_point.responses.location_point import LocationPointVM
from src.presentation.api.handlers.location_point.controllers.common.router import location_point_router

#
# @location_point_router.get('//')
# async def point_id_empty():
#     return JSONResponse(status_code=400, content={'message': 'pointId не был указан'})


@location_point_router.get('/{point_id}', response_model=LocationPointVM)
async def get_location_point(
        point_id: int,
        location_point_service: LocationPointService = Depends(location_point_provider),
        presenter: Presenter = Depends(presenter_provider),
        _: Any = Depends(optional_auth_provider),
) -> LocationPointVM:
    location_point_dto = await location_point_service.get_location_point(point_id)
    return presenter.load(LocationPointVM, location_point_dto)
