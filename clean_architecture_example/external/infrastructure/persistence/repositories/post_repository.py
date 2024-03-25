from datetime import datetime
from core.domain.posts.post import Post, PostContent, PostId, PostTitle
from core.domain.posts.repository import PostRepository
from core.domain.users.user import UserId
from external.infrastructure.persistence.repositories.mappers.post_mapper import (
    post_from_dict_to_entity,
)
from psycopg import AsyncConnection
from psycopg.rows import dict_row


class PostgresqlPostRepository(PostRepository):
    __slots__ = ("connection",)

    def __init__(self, connection: AsyncConnection) -> None:
        self.connection = connection

    async def create(self, post: Post) -> None:
        async with self.connection.cursor() as cursor:
            await cursor.execute(
                """
                INSERT INTO posts (id, title, content, owner_id, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s);
                """,
                (
                    post.id.value,
                    post.title.value,
                    post.content.value,
                    post.owner_id.value,
                    post.created_at,
                    post.updated_at,
                ),
            )

    async def find_by_id(self, id: PostId) -> Post | None:
        async with self.connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                SELECT id, title, content, owner_id, created_at, updated_at
                FROM posts
                WHERE id = %s;
                """,
                (id.value,),
            )

            result = await cursor.fetchone()

            if result is None:
                return None

            return post_from_dict_to_entity(result)

    async def find_all(self, limit: int = 20, offset: int = 0) -> list[Post] | None:
        async with self.connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                SELECT id, title, content, owner_id, created_at, updated_at
                FROM posts LIMIT %s OFFSET %s;
                """,
                (limit, offset),
            )

            result = await cursor.fetchall()

            if not result:
                return None

            return [post_from_dict_to_entity(row) for row in result]

    async def find_by_owner_id(
        self, owner_id: UserId, limit: int = 20, offset: int = 0
    ) -> list[Post] | None:
        async with self.connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                SELECT id, title, content, owner_id, created_at, updated_at
                FROM posts
                WHERE owner_id = %s
                LIMIT %s OFFSET %s;
                """,
                (owner_id.value, limit, offset),
            )

            result = await cursor.fetchall()

            if not result:
                return None

            return [post_from_dict_to_entity(row) for row in result]

    async def edit(
        self,
        id: PostId,
        title: PostTitle,
        updated_at: datetime,
        content: PostContent | None = None,
    ) -> None:
        async with self.connection.cursor() as cursor:
            if content is not None:
                query = """UPDATE posts SET title = %s, updated_at = %s, content = %s WHERE id = %s;"""
                await cursor.execute(
                    query, (title.value, updated_at, content.value, id.value)
                )

            else:
                query = (
                    """UPDATE posts SET title = %s, updated_at = %s WHERE id = %s;"""
                )
                await cursor.execute(query, (title.value, updated_at, id.value))

    async def delete(self, id: PostId) -> None:
        async with self.connection.cursor() as cursor:
            await cursor.execute("DELETE FROM posts WHERE id = %s;", (id.value,))
