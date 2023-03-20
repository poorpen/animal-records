from typing import Any

from fastapi import Depends

from src.application.animal.dto.animal_visited_location import AddAnimalVisitedLocationDTO
from src.application.animal.dto.type_of_specific_animal import AddTypeOfSpecificAnimalDTO
from src.application.animal.dto.animal import CreateAnimalDTO
from src.application.animal.usecases.animal_visited_location import AnimalVisitedLocationService
from src.application.animal.usecases.type_of_specific_animal import TypeOfSpecificAnimalService
from src.application.animal.usecases.animal import AnimalService

from src.presentation.api.providers.abstract.auth import auth_provider
from src.presentation.api.providers.abstract.services import animal_provider, type_of_specific_animal_provider, \
    visited_location_provider
from src.presentation.api.presenter.presenter import Presenter
from src.presentation.api.providers.abstract.common import presenter_provider

from src.presentation.api.handlers.animal.requests.post_reguest import CreateAnimalVM
from src.presentation.api.handlers.animal.responses.animal_visited_location import AnimalVisitedLocationVM
from src.presentation.api.handlers.animal.responses.animal import AnimalVM

from src.presentation.api.handlers.animal.controllers.common.router import animals_router


@animals_router.post('', response_model=AnimalVM, status_code=201)
async def add_animal(
        animal_data: CreateAnimalVM,
        animal_service: AnimalService = Depends(animal_provider),
        presenter: Presenter = Depends(presenter_provider),
        _: Any = Depends(auth_provider)
) -> AnimalVM:
    create_animal_dto = CreateAnimalDTO(
        animal_types=animal_data.animal_types,
        weight=animal_data.weight,
        length=animal_data.length,
        height=animal_data.height,
        gender=animal_data.gender,
        chipper_id=animal_data.chipper_id,
        chipping_location_id=animal_data.chipping_location_id
    )
    animal_dto = await animal_service.create_animal(create_animal_dto)
    return presenter.load(AnimalVM, animal_dto)


@animals_router.post('/{animal_id}/types/{type_id}', status_code=201, response_model=AnimalVM)
async def add_type_of_specific_animal(
        animal_id: int,
        type_id: int,
        specific_animal_type_service: TypeOfSpecificAnimalService = Depends(type_of_specific_animal_provider),
        presenter: Presenter = Depends(presenter_provider),
        _: Any = Depends(auth_provider)

) -> AnimalVM:
    add_type_dto = AddTypeOfSpecificAnimalDTO(
        animal_id=animal_id,
        animal_type_id=type_id
    )
    animal_dto = await specific_animal_type_service.add_type(add_type_dto)
    return presenter.load(AnimalVM, animal_dto)


@animals_router.post('/{animal_id}/locations/{point_id}', status_code=201, response_model=AnimalVisitedLocationVM)
async def add_visited_location(
        animal_id: int,
        point_id: int,
        visited_location_service: AnimalVisitedLocationService = Depends(visited_location_provider),
        presenter: Presenter = Depends(presenter_provider),
        _: Any = Depends(auth_provider)
) -> AnimalVisitedLocationVM:
    add_visited_location_dto = AddAnimalVisitedLocationDTO(
        animal_id=animal_id,
        location_point_id=point_id
    )
    visited_location_dto = await visited_location_service.add_visited_location(add_visited_location_dto)
    return presenter.load(AnimalVisitedLocationVM, visited_location_dto)
