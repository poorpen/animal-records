from typing import Any

from fastapi import Depends

from src.application.animal.dto.animal_visited_location import ChangeAnimalVisitedLocationDTO
from src.application.animal.dto.type_of_specific_animal import ChangeTypeOfSpecificAnimalDTO
from src.application.animal.dto.animal import UpdateAnimalDTO
from src.application.animal.usecases.animal import AnimalService
from src.application.animal.usecases.animal_visited_location import AnimalVisitedLocationService
from src.application.animal.usecases.type_of_specific_animal import TypeOfSpecificAnimalService

from src.presentation.api.providers.abstract.auth import auth_provider
from src.presentation.api.providers.abstract.services import animal_provider, type_of_specific_animal_provider, \
    visited_location_provider
from src.presentation.api.presenter.presenter import Presenter
from src.presentation.api.providers.abstract.common import presenter_provider

from src.presentation.api.handlers.animal.requests.put_request import UpdateAnimalVM, ChangeTypeOfSpecificAnimalVM, \
    ChangeAnimalVisitedLocationVM
from src.presentation.api.handlers.animal.responses.animal import AnimalsVM, AnimalVM
from src.presentation.api.handlers.animal.responses.animal_visited_location import AnimalVisitedLocationVM

from src.presentation.api.handlers.animal.controllers.common.router import animals_router


@animals_router.put('/{animal_id}', response_model=AnimalsVM)
async def update_animal(
        animal_id: int,
        animal_data: UpdateAnimalVM,
        animal_service: AnimalService = Depends(animal_provider),
        presenter: Presenter = Depends(presenter_provider)
) -> AnimalsVM:
    update_animal_dto = UpdateAnimalDTO(
        id=animal_id,
        weight=animal_data.weight,
        height=animal_data.height,
        length=animal_data.length,
        gender=animal_data.gender,
        life_status=animal_data.life_status,
        chipper_id=animal_data.chipper_id,
        chipping_location_id=animal_data.chipping_location_id
    )
    animal_dto = await animal_service.update_animal(update_animal_dto)
    return presenter.load(AnimalsVM, animal_dto)


@animals_router.put('/{animal_id}/types', response_model=AnimalVM)
async def change_type_of_specific_animal(
        animal_id: int,
        type_data: ChangeTypeOfSpecificAnimalVM,
        specific_animal_type_service: TypeOfSpecificAnimalService = Depends(type_of_specific_animal_provider),
        presenter: Presenter = Depends(presenter_provider),
        _: Any = Depends(auth_provider)

) -> AnimalVM:
    change_type_of_specific_animal_dto = ChangeTypeOfSpecificAnimalDTO(
        animal_id=animal_id,
        old_type_id=type_data.old_type_id,
        new_type_id=type_data.new_type_id
    )
    animal_dto = specific_animal_type_service.change_type(change_type_of_specific_animal_dto)
    return presenter.load(AnimalVM, animal_dto)


@animals_router.post('/{animal_id}/locations/{point_id}', response_model=AnimalVisitedLocationVM)
async def change_visited_location(
        animal_id: int,
        visited_location_data: ChangeAnimalVisitedLocationVM,
        visited_location_service: AnimalVisitedLocationService = Depends(visited_location_provider),
        presenter: Presenter = Depends(presenter_provider),
        _: Any = Depends(auth_provider)
) -> AnimalVisitedLocationVM:
    change_visited_location_dto = ChangeAnimalVisitedLocationDTO(
        id=visited_location_data.visited_location_point_id,
        animal_id=animal_id,
        location_point_id=visited_location_data.location_point_id
    )
    visited_location_dto = await visited_location_service.change_visited_location(change_visited_location_dto)
    return presenter.load(AnimalVisitedLocationVM, visited_location_dto)
