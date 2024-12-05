import hashlib

import jwt
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from passlib.context import CryptContext


SECRET_KEY = "98092121561"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Genera un hash SHA-256 de la contraseña proporcionada."""
    # Codificar la contraseña en bytes y calcular el hash
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password( hashed_password: str, password: str) -> bool:
    """Verifica si la contraseña proporcionada coincide con el hash almacenado."""
    return hashed_password == get_password_hash(password)


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



