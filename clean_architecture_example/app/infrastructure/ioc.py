from typing import AsyncGenerator

from dishka import Provider, Scope, from_context, provide
from fastapi import Request
from psycopg import AsyncConnection
from psycopg.conninfo import conninfo_to_dict

from app.application.common.date_time_provider import DateTimeProvider
from app.application.common.id_provider import IdProvider
from app.application.common.jwt_processor import JwtTokenProcessor
from app.application.common.password_hasher import PasswordHasher
from app.application.common.unit_of_work import UnitOfWork
from app.application.usecases.authentication.login import Login
from app.application.usecases.authentication.register import Register
from app.application.usecases.comments.create_comment import CreateComment
from app.application.usecases.comments.delete_comment import DeleteComment
from app.application.usecases.comments.get_comment import (
    GetCommentById,
    GetCommentListByPostId,
)
from app.application.usecases.posts.create_post import CreatePost
from app.application.usecases.posts.delete_post import DeletePost
from app.application.usecases.posts.get_post import GetPostById, GetPostList
from app.application.usecases.posts.update_post import UpdatePost
from app.application.usecases.users.get_current_user import GetCurrentUser
from app.domain.comments.repository import CommentRepository
from app.domain.posts.repository import PostRepository
from app.domain.users.repository import UserRepository
from app.infrastructure.authentication.id_provider import JwtTokenIdProvider
from app.infrastructure.authentication.jwt_processor import JoseJwtTokenProcessor
from app.infrastructure.authentication.jwt_settings import JwtSettings
from app.infrastructure.date_time_provider import SystemDateTimeProvider, Timezone
from app.infrastructure.persistence.db_settings import DatabaseSettings
from app.infrastructure.persistence.repositories.comment_repository import (
    PostgresqlCommentRepository,
)
from app.infrastructure.persistence.repositories.post_repository import (
    PostgresqlPostRepository,
)
from app.infrastructure.persistence.repositories.user_repository import (
    PostgresqlUserRepository,
)
from app.infrastructure.persistence.unit_of_work import PostgresqlUnitOfWork
from app.infrastructure.security.password_hasher import Pbkdf2PasswordHasher
from app.infrastructure.settings import MainSettings
from app.infrastructure.utils.get_env_var import get_env_variable


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def jwt_settings(self) -> JwtSettings:
        return JwtSettings(
            secret=get_env_variable("JWT_SECRET_KEY"),
            algorithm=get_env_variable("JWT_ALGORITHM"),
            expires_in=int(get_env_variable("JWT_EXPIRES_IN")),
        )

    @provide(scope=Scope.APP)
    def db_settings(self) -> DatabaseSettings:
        return DatabaseSettings(
            host=get_env_variable("POSTGRES_HOST"),
            port=int(get_env_variable("POSTGRES_PORT")),
            user=get_env_variable("POSTGRES_USER"),
            password=get_env_variable("POSTGRES_PASSWORD"),
            database=get_env_variable("POSTGRES_DB"),
        )

    @provide(scope=Scope.APP)
    def main_settings(
        self, jwt_settings: JwtSettings, db_settings: DatabaseSettings
    ) -> MainSettings:
        return MainSettings(
            jwt_settings=jwt_settings,
            db_settings=db_settings,
        )


class DatabaseConfigurationProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=AsyncConnection)
    async def provide_db_connection(
        self, db_settings: DatabaseSettings
    ) -> AsyncGenerator[AsyncConnection, None]:
        connection = await AsyncConnection.connect(
            **conninfo_to_dict(db_settings.uri),
        )
        yield connection
        await connection.close()


class DatabaseAdaptersProvider(Provider):
    scope = Scope.REQUEST

    unit_of_work = provide(PostgresqlUnitOfWork, provides=UnitOfWork)
    user_repository = provide(PostgresqlUserRepository, provides=UserRepository)
    post_repository = provide(PostgresqlPostRepository, provides=PostRepository)
    comment_repository = provide(
        PostgresqlCommentRepository, provides=CommentRepository
    )


class AuthenticationAdaptersProvider(Provider):
    token_processor = provide(
        JoseJwtTokenProcessor, scope=Scope.APP, provides=JwtTokenProcessor
    )
    request = from_context(
        scope=Scope.REQUEST,
        provides=Request,
    )

    @provide(scope=Scope.REQUEST, provides=IdProvider)
    def id_provider(
        self, token_processor: JwtTokenProcessor, request: Request
    ) -> IdProvider:
        return JwtTokenIdProvider(token_processor=token_processor, token=request.auth)


class SecurityProvider(Provider):
    scope = Scope.APP
    password_hasher = provide(Pbkdf2PasswordHasher, provides=PasswordHasher)


class DateTimeProvider(Provider):
    @provide(scope=Scope.APP, provides=DateTimeProvider)
    def provide_date_time_provider(self) -> DateTimeProvider:
        return SystemDateTimeProvider(Timezone.UTC)


class UseCasesProvider(Provider):
    scope = Scope.REQUEST

    login = provide(Login)
    register = provide(Register)
    get_current_user = provide(GetCurrentUser)
    create_post = provide(CreatePost)
    get_post_by_id = provide(GetPostById)
    get_post_list = provide(GetPostList)
    update_post = provide(UpdatePost)
    delete_post = provide(DeletePost)
    create_comment = provide(CreateComment)
    get_comment_by_id = provide(GetCommentById)
    get_comment_list_by_post_id = provide(GetCommentListByPostId)
    delete_comment = provide(DeleteComment)


PROVIDERS: list[Provider] = [
    SettingsProvider(),
    DatabaseConfigurationProvider(),
    DatabaseAdaptersProvider(),
    AuthenticationAdaptersProvider(),
    SecurityProvider(),
    UseCasesProvider(),
    DateTimeProvider(),
]
