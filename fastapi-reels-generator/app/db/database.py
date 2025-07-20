from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
# app/database.py
from app.config import DB_CONNECTION
from app.users.schema import User
from app.reels.schema import Reel

class Database:
    def __init__(self, connection_string=DB_CONNECTION):
        self.engine = create_async_engine(connection_string)
        self.Session = async_sessionmaker(bind=self.engine)

    async def init_db(self):
        from app.users import User
        from app.reels import Reel
        async with self.engine.begin() as conn:
            await conn.run_sync(User.metadata.create_all)
            await conn.run_sync(Reel.metadata.create_all)

    async def get_session(self) -> AsyncSession:
        return self.Session()

    async def close(self):
        await self.engine.dispose()