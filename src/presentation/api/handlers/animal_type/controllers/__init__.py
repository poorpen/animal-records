from .common import animal_type_exception_handler

from .get_controllers import animal_type_router
from .post_controllers import animal_type_router
from .put_controllers import animal_type_router
from .delete_controllers import animal_type_router

__all__ = ['animal_type_router', 'animal_type_exception_handler']
