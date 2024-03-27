from app.web_api.routers.auth import auth_router
from app.web_api.routers.comment import comment_router
from app.web_api.routers.post import post_router
from app.web_api.routers.user import user_router

__all__ = [
    "user_router",
    "auth_router",
    "post_router",
    "comment_router",
]
