from typing import Any

from fastapi import Depends

from src.application.animal_type.dto.animal_type import CreateAnimalTypeDTO
from src.application.animal_type.usecases.animal_type import AnimalTypeService

from src.presentation.api.providers.abstract.auth import auth_provider
from src.presentation.api.providers.abstract.services import animal_type_provider

from src.presentation.api.providers.abstract.common import presenter_provider
from src.presentation.api.presenter.presenter import Presenter

from src.presentation.api.handlers.animal_type.requests.post_request import CreateAnimalTypeVM
from src.presentation.api.handlers.animal_type.responses.animal_type import AnimalTypeVM

from src.presentation.api.handlers.animal_type.controllers.common.router import animal_type_router


@animal_type_router.post('', response_model=AnimalTypeVM, status_code=201)
async def create_animal_type(
        animal_type_data: CreateAnimalTypeVM,
        animal_type_service: AnimalTypeService = Depends(animal_type_provider),
        presenter: Presenter = Depends(presenter_provider),
        _: Any = Depends(auth_provider)
) -> AnimalTypeVM:
    create_type_dto = CreateAnimalTypeDTO(
        type=animal_type_data.animal_type
    )
    type_dto = await animal_type_service.create_animal_type(create_type_dto)
    return presenter.load(AnimalTypeVM, type_dto)
