from app.infrastructure.ioc import create_container
from app.web_api.exc_handlers import init_exc_handlers
from app.web_api.routers import auth_router, comment_router, post_router, user_router

from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka


def init_di(app: FastAPI) -> None:
    container = create_container()
    setup_dishka(container, app)


def init_routers(app: FastAPI) -> None:
    app.include_router(user_router)
    app.include_router(auth_router)
    app.include_router(post_router)
    app.include_router(comment_router)


def app_factory() -> FastAPI:
    app = FastAPI()

    init_di(app)
    init_routers(app)
    init_exc_handlers(app)

    return app
