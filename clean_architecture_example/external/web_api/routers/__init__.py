from external.web_api.routers.auth import auth_router
from external.web_api.routers.post import post_router
from external.web_api.routers.user import user_router

__all__ = [
    "user_router",
    "auth_router",
    "post_router",
]
