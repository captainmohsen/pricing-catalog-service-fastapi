from datetime import datetime, timedelta
from typing import Any, Union
from app.core.config import settings
from jose import jwt
from passlib.context import CryptContext
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
import re


import logging

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def create_token(user_session: str, user_id: str, first_name: str, last_name: str, email: str, role: str,
                 expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "session": user_session, "user_id":str(user_id),
                 "email":email}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_access_token(
        subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


#TODO this validation should be complete better
def validate_password(password: str) -> None:
    if len(password) < 8 or not re.search(r'\d', password):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters and contain a number."
        )