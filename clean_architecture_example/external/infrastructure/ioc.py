from typing import AsyncGenerator

from core.application.common.date_time_provider import DateTimeProvider
from core.application.common.jwt_processor import JwtTokenProcessor
from core.application.common.password_hasher import PasswordHasher
from core.application.common.unit_of_work import UnitOfWork
from core.application.common.id_provider import IdProvider
from core.application.usecases.authentication.login import Login
from core.application.usecases.authentication.register import Register
from core.application.usecases.posts.create_post import CreatePost
from core.application.usecases.posts.delete_post import DeletePost
from core.application.usecases.posts.get_posts import (
    GetPostById,
    GetPostList,
    GetPostListByOwnerId,
)
from core.application.usecases.posts.update_post import UpdatePost
from core.application.usecases.users.get_current_user import GetCurrentUser
from core.domain.posts.repository import PostRepository
from core.domain.users.repository import UserRepository
from dishka import Provider, Scope, from_context, provide
from external.infrastructure.authentication.jwt_processor import JoseJwtTokenProcessor
from external.infrastructure.authentication.jwt_settings import JwtSettings
from external.infrastructure.authentication.id_provider import JwtTokenIdProvider
from external.infrastructure.patterns.date_time_provider import (
    SystemDateTimeProvider,
    Timezone,
)
from external.infrastructure.persistence.db_settings import DatabaseSettings
from external.infrastructure.persistence.repositories.post_repository import (
    PostgresqlPostRepository,
)
from external.infrastructure.persistence.repositories.user_repository import (
    PostgresqlUserRepository,
)
from external.infrastructure.persistence.unit_of_work import PostgresqlUnitOfWork
from external.infrastructure.security.password_hasher import Pbkdf2PasswordHasher
from external.infrastructure.settings import MainSettings
from external.infrastructure.utils.get_env_var import get_env_variable
from fastapi import Request
from psycopg import AsyncConnection
from psycopg.conninfo import conninfo_to_dict


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
            host=get_env_variable("DB_HOST"),
            port=int(get_env_variable("DB_PORT")),
            user=get_env_variable("DB_USER"),
            password=get_env_variable("DB_PASSWORD"),
            database=get_env_variable("DB_NAME"),
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


class PatternsProvider(Provider):
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
    get_post_list_by_owner_id = provide(GetPostListByOwnerId)
    update_post = provide(UpdatePost)
    delete_post = provide(DeletePost)


PROVIDERS: list[Provider] = [
    SettingsProvider(),
    DatabaseConfigurationProvider(),
    DatabaseAdaptersProvider(),
    AuthenticationAdaptersProvider(),
    SecurityProvider(),
    UseCasesProvider(),
    PatternsProvider(),
]
