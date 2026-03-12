from asyncpg import Connection
from asyncpg.transaction import Transaction

from src.database.dbmanager import get_pool


class UoW:

    def __init__(self, conn: Connection | None = None):
        self._export_conn = conn
        self.conn: Connection | None = conn

    async def __aenter__(self):
        if not self.conn:
            self.conn = await get_pool().acquire()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not self._export_conn:
            await get_pool().release(self.conn)

    async def get_conn(self):
        if not self.conn:
            raise RuntimeError("UoW not entered. Use 'async with UoW() as uow:' first.")
        return self.conn

    class _TransactionContext:
        def __init__(self, conn: Connection):
            self.conn = conn
            self._tx: Transaction | None = None

        async def __aenter__(self):
            self._tx = self.conn.transaction()
            await self._tx.start()
            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            if self._tx is not None:
                if exc_type:
                    await self._tx.rollback()
                else:
                    await self._tx.commit()

    def transaction(self):
        if self.conn is None:
            raise RuntimeError("UoW not entered. Use 'async with UoW() as uow:' first.")
        return self._TransactionContext(self.conn)
