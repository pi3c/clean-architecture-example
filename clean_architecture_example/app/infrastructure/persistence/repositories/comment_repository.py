from datetime import datetime

from app.domain.comments.comment import Comment, CommentContent, CommentId
from app.domain.comments.repository import CommentRepository
from app.domain.posts.post import PostId
from app.infrastructure.persistence.repositories.mappers.comment_mapper import (
    comment_from_dict_to_entity,
)
from psycopg import AsyncConnection
from psycopg.rows import dict_row


class PostgresqlCommentRepository(CommentRepository):
    __slots__ = ("connection",)

    def __init__(self, connection: AsyncConnection) -> None:
        self.connection = connection

    async def create(self, comment: Comment) -> None:
        async with self.connection.cursor() as cursor:
            await cursor.execute(
                """
                INSERT INTO comments (id, content, post_id, owner_id, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s);
                """,
                (
                    comment.id.value,
                    comment.content.value,
                    comment.post_id.value,
                    comment.owner_id.value,
                    comment.created_at,
                    comment.updated_at,
                ),
            )

    async def update(
        self,
        id: CommentId,
        content: CommentContent,
        updated_at: datetime,
    ) -> None:
        async with self.connection.cursor() as cursor:
            if content is not None:
                query = """UPDATE comments SET updated_at = %s, content = %s WHERE id = %s;"""
                await cursor.execute(query, (updated_at, content.value, id.value))

    async def find_by_id(self, id: CommentId) -> Comment | None:
        async with self.connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                SELECT id, content, post_id, owner_id, created_at, updated_at
                FROM comments
                WHERE id = %s;
                """,
                (id.value,),
            )

            result = await cursor.fetchone()

            if result is None:
                return None

            return comment_from_dict_to_entity(result)

    async def find_by_post_id(
        self, post_id: PostId, limit: int = 20, offset: int = 0
    ) -> list[Comment] | None:
        async with self.connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                SELECT id, content, post_id, owner_id, created_at, updated_at
                FROM comments
                WHERE post_id = %s
                LIMIT %s OFFSET %s;
                """,
                (post_id.value, limit, offset),
            )

            result = await cursor.fetchall()

            if not result:
                return None

            return [comment_from_dict_to_entity(row) for row in result]

    async def delete(self, id: CommentId) -> None:
        async with self.connection.cursor() as cursor:
            await cursor.execute("DELETE FROM comments WHERE id = %s;", (id.value,))
