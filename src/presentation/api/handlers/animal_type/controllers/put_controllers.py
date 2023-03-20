from typing import Any

from fastapi import Depends

from src.application.animal_type.dto.animal_type import ChangeAnimalTypeDTO
from src.application.animal_type.usecases.animal_type import AnimalTypeService

from src.presentation.api.providers.abstract.auth import auth_provider
from src.presentation.api.providers.abstract.services import animal_type_provider

from src.presentation.api.providers.abstract.common import presenter_provider
from src.presentation.api.presenter.presenter import Presenter

from src.presentation.api.handlers.animal_type.requests.put_request import ChangeAnimalTypeVM
from src.presentation.api.handlers.animal_type.responses.animal_type import AnimalTypeVM

from src.presentation.api.handlers.animal_type.controllers.common.router import animal_type_router


@animal_type_router.put('/{type_id}', response_model=AnimalTypeVM)
async def create_animal_type(
        type_id: int,
        animal_type_data: ChangeAnimalTypeVM,
        animal_type_service: AnimalTypeService = Depends(animal_type_provider),
        presenter: Presenter = Depends(presenter_provider),
        _: Any = Depends(auth_provider)
) -> AnimalTypeVM:
    change_animal_type_dto = ChangeAnimalTypeDTO(
        id=type_id,
        type=animal_type_data.animal_type

    )
    animal_type_dto = await animal_type_service.change_animal_type(change_animal_type_dto)
    return presenter.load(AnimalTypeVM, animal_type_dto)
