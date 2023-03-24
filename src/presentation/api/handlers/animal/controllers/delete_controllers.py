from typing import Any

from fastapi import Depends
from fastapi.responses import JSONResponse

from src.application.animal.usecases.animal import AnimalService
from src.application.animal.usecases.animal_visited_location import AnimalVisitedLocationService
from src.application.animal.usecases.type_of_specific_animal import TypeOfSpecificAnimalService

from src.presentation.api.providers.abstract.auth import auth_provider
from src.presentation.api.providers.abstract.services import animal_provider, type_of_specific_animal_provider, \
    visited_location_provider
from src.presentation.api.presenter.presenter import Presenter
from src.presentation.api.providers.abstract.common import presenter_provider
from src.presentation.api.handlers.animal.responses.animal import AnimalVM

from src.presentation.api.handlers.animal.controllers.common.router import animals_router


@animals_router.delete('/{animal_id}')
async def delete_animal(
        animal_id: int,
        animal_service: AnimalService = Depends(animal_provider),
        _: Any = Depends(auth_provider)) -> JSONResponse:
    await animal_service.delete_animal(animal_id)
    return JSONResponse(status_code=200, content={'message': "Запрос успешно выполнен"})


@animals_router.delete('/{animal_id}/types/{type_id}', response_model=AnimalVM)
async def delete_animal_type_of_specific_animal(
        animal_id: int,
        type_id: int,
        specific_animal_type_service: TypeOfSpecificAnimalService = Depends(type_of_specific_animal_provider),
        presenter: Presenter = Depends(presenter_provider),
        _: Any = Depends(auth_provider)) -> AnimalVM:
    animal_dto = await specific_animal_type_service.delete_type(animal_id=animal_id, animal_type_id=type_id)
    return presenter.load(AnimalVM, animal_dto)


@animals_router.delete('/{animal_id}/locations/{visited_location_id}')
async def delete_visited_locations(
        animal_id: int,
        visited_location_id: int,
        visited_location_service: AnimalVisitedLocationService = Depends(visited_location_provider),
        _: Any = Depends(auth_provider)
) -> JSONResponse:
    await visited_location_service.delete_visited_location(animal_id=animal_id, visited_location_id=visited_location_id)
    return JSONResponse(status_code=200, content={'message': "Запрос успешно выполнен"})
