import logging
from functools import partial
from types import MappingProxyType
from typing import Mapping

from aiohttp import PAYLOAD_REGISTRY
from aiohttp.payload import JsonPayload
from aiohttp.web_app import Application
from aiohttp_apispec import setup_aiohttp_apispec
from aiohttp_swagger import setup_swagger
from configargparse import Namespace

from ..urls import ROUTERS_LIST
from ..utils.pg import setup_pg
from .middlewares import error_middleware, params_middleware

GIGABYTE = 1024 ** 3
MAX_REQUEST_SIZE = 2 * GIGABYTE

log = logging.getLogger(__name__)


def create_app(args: Namespace) -> Application:
    """Создает экземпляр приложения, готового к запуску."""
    app = Application(
        client_max_size=MAX_REQUEST_SIZE,
        middlewares=[error_middleware, params_middleware],
    )
    # Swagger документация
    setup_aiohttp_apispec(
        app=app,
        title="Поиск любого кино и актеров",
        swagger_path="/api/docs",
    )

    # setup_swagger(
    #     app, swagger_from_file="swagger3.yaml", ui_version=3, swagger_url="/docs"
    # )
    # Подключение на старте к postgres и отключение при остановке
    app.cleanup_ctx.append(partial(setup_pg, args=args))

    for router in ROUTERS_LIST:
        app.router.add_routes(router)

    PAYLOAD_REGISTRY.register(JsonPayload, (Mapping, MappingProxyType))

    return app
