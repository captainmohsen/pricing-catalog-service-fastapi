import logging
from typing import Any, Dict, Generator, Optional
import redis
from app import models, schemas
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal
from fastapi import Body, Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette.requests import Request
from ua_parser import user_agent_parser
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

# from app.core.token import verify_token
from sqlalchemy.orm import sessionmaker

import json
from sqlalchemy.ext.asyncio import AsyncSession

from redis.asyncio import Redis

from contextlib import asynccontextmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from sqlalchemy.future import select
engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, future=True, connect_args=settings.connect_args)
async_session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/access_token/"
)


async def  get_db() -> AsyncGenerator[Any, Any, Any]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        finally:
            await session.close()


# @asynccontextmanager
# async def get_db() -> AsyncSession:
#     """Provide a transactional scope for asynchronous database session."""
#     async with SessionLocal() as db:
#         try:
#             print("db opened")
#             yield db
#         finally:
#             db.close()
#             print("db closed")




@asynccontextmanager
async def get_redis_conn() -> Redis:
    """
    Provides an async Redis connection using aioredis.
    """
    redis_conn = await Redis.from_url(f"redis://{settings.REDIS_SERVER}")
    try:
        yield redis_conn
    finally:
        await redis_conn.close()

# async def login_activity_from_request(*, request: Request):
#     user_agent = user_agent_parser.Parse(request.headers.get('user-agent'))
#     os = user_agent['os']['family'].replace("None", '')
#     browser = user_agent['user_agent']['family'].replace("None", '')
#     browser_version = f"{user_agent['user_agent']['major']}.{user_agent['user_agent']['minor']}.{user_agent['user_agent']['patch']}".replace(
#         "None", '')
#
#     return LoginActivity(platform=os, browser=browser + ':' + browser_version, user_ip=request.client.host)

#
# def verify_token(token: str):
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
#         session_data = payload['session']
#         try:
#             redis_conn = redis.StrictRedis(host=settings.REDIS_HOST)
#             user_data = redis_conn.get(session_data)
#             if user_data is not None:
#                 return dict(verified=True, user_data=json.loads(user_data))
#         finally:
#             redis_conn.close()
#
#         db = SessionLocal()
#         # with get_db1() as db:
#         user_session = db.query(UserSession) \
#             .filter(UserSession.session_data == session_data).scalar()
#         if not user_session:
#             raise Exception('session not found')
#         if user_session.is_revoked:
#             raise Exception('session revoked')
#         # user = crud.user.get_by_id(db=db,user_id=user_session.user_id)
#         return dict(verified=True, user_data=crud.user.get_user_data(db=db, user_id=user_session.user_id))
#
#     except (jwt.JWTError, Exception) as e:
#         print(e)
#         return dict(verified=False, user_data=None)


# async def get_current_user_token(
#         db: AsyncSession = Depends(get_db), token: str = Depends(reusable_oauth2)
# ) -> models.User:
#     token_verify = verify_token(token)
#     if not token_verify["verified"]:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#         )
#
#     user = await  crud.user.get(db, id=token_verify["user_data"]["id"])
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return token
#

#
# async def get_current_user(
#         db: AsyncSession = Depends(get_db), token: str = Depends(reusable_oauth2)
# ) -> models.User:
#     token_verify = verify_token(token)
#     if not token_verify["verified"]:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#         )
#
#     user = await crud.user.get(db, id=token_verify["user_data"]["id"])
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user
#
#
# async def get_current_active_user(
#         current_user: models.User = Depends(get_current_user),
# ) -> models.User:
#     if not await crud.user.is_active(current_user):
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
#
#
#
#
#
# async def get_current_active_admin(
#         current_user: models.User = Depends(get_current_user),
#         db: AsyncSession = Depends(get_db),
# ) -> models.User:
#     # Explicitly fetch the role if it's a relationship
#     if not current_user.role_id:
#         raise HTTPException(
#             status_code=401, detail="The user doesn't have enough privileges"
#         )
#
#     role = await db.scalar(select(models.Role).where(models.Role.id == current_user.role_id))
#
#     if role and role.name == "SUPER_ADMIN":
#         return current_user
#
#     raise HTTPException(
#         status_code=401, detail="The user doesn't have enough privileges"
#     )
#
# async def get_current_active_chatbot(
#         current_user: models.User = Depends(get_current_user),
#         db: AsyncSession = Depends(get_db),
# ) -> models.User:
#     # Explicitly fetch the role if it's a relationship
#     if not current_user.role_id:
#         raise HTTPException(
#             status_code=403, detail="The user doesn't have enough privileges"
#         )
#
#     role = await db.scalar(select(models.Role).where(models.Role.id == current_user.role_id))
#
#     if role and role.name == "CHATBOT":
#         return current_user
#
#     raise HTTPException(
#         status_code=403, detail="The user doesn't have enough privileges"
#     )
#
# async def get_current_active_chatbot_admin(
#         current_user: models.User = Depends(get_current_user),
#         db: AsyncSession = Depends(get_db),
# ) -> models.User:
#
#     role = await db.scalar(select(models.Role).where(models.Role.id == current_user.role_id))
#
#     if role and role.name in ["CHATBOT", "SUPER_ADMIN"]:
#         return current_user
#
#     raise HTTPException(
#         status_code=401, detail="The user doesn't have enough privileges"
#     )
#
# async def get_current_active_customer_admin(
#         current_user: models.User = Depends(get_current_user),
#         db: AsyncSession = Depends(get_db),
# ) -> models.User:
#
#     role = await db.scalar(select(models.Role).where(models.Role.id == current_user.role_id))
#
#     if role and role.name in ["CLIENT", "SUPER_ADMIN"]:
#         return current_user
#
#     raise HTTPException(
#         status_code=401, detail="The user doesn't have enough privileges"
#     )
#
# def get_site_origin(site_origin: str = Header(...)):
#     return site_origin
#
