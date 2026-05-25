"""
Database connection and session management.
Uses Supabase client + SQLAlchemy for complex queries.
"""

from supabase import create_client, Client
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# Supabase Client
supabase: Client = None


def get_supabase() -> Client:
    """Get or create Supabase client."""
    global supabase
    if supabase is None and settings.SUPABASE_URL:
        supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    return supabase


# SQLAlchemy (for complex queries)
Base = declarative_base()

engine = None
async_session = None


def init_db():
    """Initialize database engine."""
    global engine, async_session
    if settings.DATABASE_URL:
        engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)
        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncSession:
    """Get database session."""
    if async_session is None:
        init_db()
    async with async_session() as session:
        yield session
