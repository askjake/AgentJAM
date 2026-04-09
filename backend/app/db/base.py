"""
Database base configuration and session management
"""
import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase
from contextlib import asynccontextmanager

# Get database URL from environment
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql+asyncpg://dishchat:dishchat@localhost/dishchat'
)

class Base(DeclarativeBase):
    """Base class for all models"""
    pass

class DatabaseSessionManager:
    """Manage database connections and sessions"""
    
    def __init__(self, url: str):
        self.engine = create_async_engine(
            url,
            echo=False,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20
        )
        self.session_maker = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
    
    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get a database session"""
        async with self.session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
    
    @asynccontextmanager
    async def connect(self):
        """Get a raw connection"""
        async with self.engine.begin() as conn:
            yield conn
    
    async def close(self):
        """Close all connections"""
        await self.engine.dispose()

# Global session manager
sessionmanager = DatabaseSessionManager(DATABASE_URL)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for FastAPI/Flask routes"""
    async with sessionmanager.session() as session:
        yield session
