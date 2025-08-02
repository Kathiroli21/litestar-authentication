from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

from my_app.db import SessionLocal

@asynccontextmanager
async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
