from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker


engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, future=True, connect_args=settings.connect_args)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

sync_engine =  create_engine(settings.SQLALCHEMY_SYNC_DATABASE_URI, echo=False)
SyncSessionLocal = sessionmaker(bind=sync_engine)





