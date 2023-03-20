from typing import Any

from fastapi import Depends

from src.application.location_point.dto.location_point import CreateLocationPointDTO
from src.application.location_point.usecases.location_point import LocationPointService

from src.presentation.api.providers.abstract.auth import auth_provider
from src.presentation.api.providers.abstract.services import location_point_provider

from src.presentation.api.providers.abstract.common import presenter_provider
from src.presentation.api.presenter.presenter import Presenter

from src.presentation.api.handlers.location_point.requests.post_request import CreateLocationPointVM
from src.presentation.api.handlers.location_point.responses.location_point import LocationPointVM

from src.presentation.api.handlers.location_point.controllers.common.router import location_point_router


@location_point_router.post('', status_code=201, response_model=LocationPointVM)
async def create_location_point(
        location_point_data: CreateLocationPointVM,
        location_point_service: LocationPointService = Depends(location_point_provider),
        presenter: Presenter = Depends(presenter_provider),
        _: Any = Depends(auth_provider)
) -> LocationPointVM:
    create_location_point_dto = CreateLocationPointDTO(
        latitude=location_point_data.latitude,
        longitude=location_point_data.longitude
    )
    location_point_dto = await location_point_service.create_location_point(create_location_point_dto)
    return presenter.load(LocationPointVM, location_point_dto)
