from fastapi import FastAPI

from src.presentation.api.providers import bind_providers
from src.presentation.api.handlers import bind_exception_handlers, bind_routers
from src.presentation.config.config import Config


def init_app(app: FastAPI, config: Config) -> FastAPI:
    bind_providers(app, config)
    bind_exception_handlers(app)
    bind_routers(app)
    return app
