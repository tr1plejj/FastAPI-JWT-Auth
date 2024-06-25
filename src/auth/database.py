from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.auth.config import settings

async_engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=True,
)

async_session = async_sessionmaker(async_engine)
