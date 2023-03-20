from typing import Any

from fastapi import Depends

from fastapi.responses import JSONResponse

from src.application.animal_type.usecases.animal_type import AnimalTypeService

from src.presentation.api.presenter.presenter import Presenter
from src.presentation.api.providers.abstract.auth import optional_auth_provider
from src.presentation.api.providers.abstract.common import presenter_provider
from src.presentation.api.providers.abstract.services import animal_type_provider

from src.presentation.api.handlers.animal_type.responses.animal_type import AnimalTypeVM
from src.presentation.api.handlers.animal_type.controllers.common.router import animal_type_router

#
# @animal_type_router.get('//')
# async def type_id_empty():
#     return JSONResponse(status_code=400, content={'message': 'typeId не был указан'})


@animal_type_router.get('/{type_id}', response_model=AnimalTypeVM)
async def get_animal_type(
        type_id: int,
        animal_type_service: AnimalTypeService = Depends(animal_type_provider),
        presenter: Presenter = Depends(presenter_provider),
        _: Any = Depends(optional_auth_provider),
) -> AnimalTypeVM:
    animal_type_dto = await animal_type_service.get_animal_type(type_id)
    return presenter.load(AnimalTypeVM, animal_type_dto)
