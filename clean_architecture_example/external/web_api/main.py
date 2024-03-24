from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from external.infrastructure.ioc import PROVIDERS
from external.web_api.exc_handlers import HANDLERS
from external.web_api.extensions.rate_limit import init_limiter
from external.web_api.routers import auth_router, post_router, user_router
from fastapi import FastAPI


def init_di(app: FastAPI) -> None:
    container = make_async_container(*PROVIDERS)
    setup_dishka(container, app)


def init_routers(app: FastAPI) -> None:
    app.include_router(user_router)
    app.include_router(auth_router)
    app.include_router(post_router)


def init_exc_handlers(app: FastAPI) -> None:
    for exc, handler in HANDLERS.items():
        app.add_exception_handler(exc, handler)


def app_factory() -> FastAPI:
    app = FastAPI()

    init_di(app)
    init_routers(app)
    init_exc_handlers(app)
    init_limiter(app)

    return app
