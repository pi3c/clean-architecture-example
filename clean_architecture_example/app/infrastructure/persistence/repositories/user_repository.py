from app.domain.users.repository import UserRepository
from app.domain.users.user import User, UserEmail, UserId
from app.infrastructure.persistence.repositories.mappers.user_mapper import (
    user_from_dict_to_entity,
)
from psycopg import AsyncConnection
from psycopg.rows import dict_row


class PostgresqlUserRepository(UserRepository):
    __slots__ = ("connection",)

    def __init__(self, connection: AsyncConnection) -> None:
        self.connection = connection

    async def create(self, user: User) -> None:
        async with self.connection.cursor() as cursor:
            await cursor.execute(
                """
                INSERT INTO users (id, first_name, last_name, email, hashed_password)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    user.id.value,
                    user.first_name.value,
                    user.last_name.value,
                    user.email.value,
                    user.hashed_password,
                ),
            )

    async def find_by_id(self, id: UserId) -> User | None:
        async with self.connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                SELECT id, first_name, last_name, email, hashed_password
                FROM users
                WHERE id = %s
                """,
                (id.value,),
            )
            row = await cursor.fetchone()

            if not row:
                return None

            return user_from_dict_to_entity(row)

    async def find_by_email(self, email: UserEmail) -> User | None:
        async with self.connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                SELECT id, first_name, last_name, email, hashed_password
                FROM users
                WHERE email = %s
                """,
                (email.value,),
            )
            row = await cursor.fetchone()

            if not row:
                return None

            return user_from_dict_to_entity(row)
