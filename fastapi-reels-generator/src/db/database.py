from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.env import DB_CONNECTION

class Base(DeclarativeBase):
    """Abstract base model with a common id column"""
    id: Mapped[int] = mapped_column(primary_key=True)
    
class Database:
    def __init__(self, connection_string=DB_CONNECTION):
        print(connection_string)
        self.engine = create_async_engine(connection_string)
        self.Session = async_sessionmaker(bind=self.engine)

    async def init_db(self):
        async with self.engine.begin() as conn:
                        
            from src.app.users.schema import User
            from src.app.reels.schema import Reel
            await conn.run_sync(Reel.metadata.create_all)
            await conn.run_sync(User.metadata.create_all)

    async def get_session(self) -> AsyncSession:
        return self.Session()

    async def close(self):
        await self.engine.dispose()