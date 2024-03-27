from psycopg import AsyncConnection

from app.application.common.unit_of_work import UnitOfWork


class PostgresqlUnitOfWork(UnitOfWork):
    __slots__ = ("connection",)

    def __init__(self, connection: AsyncConnection) -> None:
        self.connection = connection

    async def commit(self) -> None:
        await self.connection.commit()

    async def rollback(self) -> None:
        await self.connection.rollback()
