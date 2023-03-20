from typing import Any, Optional, List

from fastapi import Depends, Request

from src.application.animal.dto.animal_visited_location import SearchParametersVisitedLocationsDTO
from src.application.animal.dto.animal import SearchParametersDTO
from src.application.animal.usecases.animal_visited_location import AnimalVisitedLocationService
from src.application.animal.usecases.animal import AnimalService
from src.presentation.api.handlers.common.utils.from_getter import from_getter

from src.presentation.api.providers.abstract.auth import optional_auth_provider
from src.presentation.api.providers.abstract.services import animal_provider, visited_location_provider
from src.presentation.api.presenter.presenter import Presenter
from src.presentation.api.providers.abstract.common import presenter_provider

from src.presentation.api.handlers.animal.requests.get_request import SearchAnimalParametersVM, \
    SearchAnimalVisitedLocationParametersVM
from src.presentation.api.handlers.animal.responses.animal import AnimalVM, AnimalsVM
from src.presentation.api.handlers.animal.responses.animal_visited_location import AnimaVisitedLocationsVM

from src.presentation.api.handlers.animal.controllers.common.router import animals_router


@animals_router.get('/search')
async def search_animals(
        request: Request,
        search_parameters: SearchAnimalParametersVM = Depends(),
        animal_service: AnimalService = Depends(animal_provider),
        presenter: Presenter = Depends(presenter_provider),
        _: Any = Depends(optional_auth_provider),

) -> List[AnimalVM]:
    from_getter(request=request, model=search_parameters)
    search_parameters_dto = SearchParametersDTO(
        start_datetime=search_parameters.start_datetime,
        end_datetime=search_parameters.end_datetime,
        life_status=search_parameters.life_status,
        gender=search_parameters.gender,
        chipper_id=search_parameters.chipper_id,
        chipping_location_id=search_parameters.chipping_location_id,
        offset=search_parameters.offset,
        limit=search_parameters.limit

    )
    animals_dto = await animal_service.search_animal(search_parameters_dto)
    return presenter.load(AnimalsVM, animals_dto).animals


@animals_router.get('/{animal_id}', response_model=AnimalVM)
async def get_animal(
        animal_id: Optional[int],
        animal_service: AnimalService = Depends(animal_provider),
        presenter: Presenter = Depends(presenter_provider),
        _: Any = Depends(optional_auth_provider),
) -> AnimalVM:
    animal_dto = await animal_service.get_animal(animal_id)
    return presenter.load(AnimalVM, animal_dto)


@animals_router.get('/{animal_id}/locations')
async def get_animal_visited_locations(
        request: Request,
        animal_id: int,
        search_visited_locations: SearchAnimalVisitedLocationParametersVM = Depends(),
        visited_location_service: AnimalVisitedLocationService = Depends(visited_location_provider),
        presenter: Presenter = Depends(presenter_provider),
        _: Any = Depends(optional_auth_provider),
) -> list:
    from_getter(request=request, model=search_visited_locations)
    search_parameters_dto = SearchParametersVisitedLocationsDTO(
        animal_id=animal_id,
        start_datetime=search_visited_locations.start_datetime,
        end_datetime=search_visited_locations.end_datetime,
        offset=search_visited_locations.offset,
        limit=search_visited_locations.limit,
    )
    visited_locations_dto = await visited_location_service.get_visited_locations(search_parameters_dto)
    return presenter.load(AnimaVisitedLocationsVM, visited_locations_dto).visited_locations
