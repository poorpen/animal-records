from typing import Any

from fastapi import Depends
from fastapi.responses import JSONResponse

from src.application.animal_type.usecases.animal_type import AnimalTypeService

from src.presentation.api.providers.abstract.auth import auth_provider
from src.presentation.api.providers.abstract.services import animal_type_provider

from src.presentation.api.handlers.animal_type.controllers.common.router import animal_type_router


@animal_type_router.delete('/{type_id}')
async def delete_animal_type(
        type_id: int,
        animal_type_service: AnimalTypeService = Depends(animal_type_provider),
        _: Any = Depends(auth_provider)
) -> JSONResponse:
    await animal_type_service.delete_animal_type(type_id)
    return JSONResponse(status_code=200, content={'message': "Запрос успешно выполнен"})
