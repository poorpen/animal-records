import uvicorn as u
from fastapi import FastAPI
from fastapi.security import HTTPBasic

from src.presentation.api.optional_auth import OptionalAuthorizationBasic
from src.presentation.config.config_reader import config_loader
from src.presentation.api import init_app

if __name__ == '__main__':
    config = config_loader()
    app = init_app(FastAPI(), config)
    u.run(app, host=config.api.host, port=config.api.port)
