from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from Models.models import Base
import os


engine = create_async_engine(os.getenv('DB_URL'))

async_session = sessionmaker(bind=engine,
                             class_=AsyncSession,
                             expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
