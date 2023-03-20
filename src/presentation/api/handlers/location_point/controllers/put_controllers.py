from typing import Any

from fastapi import Depends

from src.application.location_point.dto.location_point import ChangeLocationPointDTO
from src.application.location_point.usecases.location_point import LocationPointService

from src.presentation.api.providers.abstract.auth import auth_provider
from src.presentation.api.providers.abstract.services import location_point_provider

from src.presentation.api.providers.abstract.common import presenter_provider
from src.presentation.api.presenter.presenter import Presenter

from src.presentation.api.handlers.location_point.requests.put_request import ChangeLocationPointVM
from src.presentation.api.handlers.location_point.responses.location_point import LocationPointVM

from src.presentation.api.handlers.location_point.controllers.common.router import location_point_router


@location_point_router.put('/{point_id}', response_model=LocationPointVM)
async def change_location_point(
        point_id: int,
        location_point_data: ChangeLocationPointVM,
        location_point_service: LocationPointService = Depends(location_point_provider),
        presenter: Presenter = Depends(presenter_provider),
        _: Any = Depends(auth_provider)
) -> LocationPointVM:
    change_location_point_dto = ChangeLocationPointDTO(
        id=point_id,
        latitude=location_point_data.latitude,
        longitude=location_point_data.longitude
    )
    location_point_dto = await location_point_service.change_location_point(change_location_point_dto)
    return presenter.load(LocationPointVM, location_point_dto)
