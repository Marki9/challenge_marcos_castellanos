# from datetime import datetime, timedelta, timezone
# from typing import Union
#
# import jwt
# from fastapi import Depends, FastAPI, HTTPException, Security, status
# from fastapi.security import (
#     OAuth2PasswordBearer,
#     OAuth2PasswordRequestForm,
#     SecurityScopes,
# )
# from jwt.exceptions import InvalidTokenError
# from passlib.context import CryptContext
# from pydantic import BaseModel, ValidationError
# from sqlalchemy.ext.asyncio import AsyncSession
# from apps.api import oauth2_scheme
# from apps.auth.tokenData import TokenData
# from apps.db.models.user import User
#
# KEY_TOKEN = "__CHALLENGE__"  # Cambia esto por una clave secreta más segura
# ALGORITHM= "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60
#
# def create_access_token(data: dict, expires_delta: timedelta ):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, KEY_TOKEN, algorithm=ALGORITHM)
#     return encoded_jwt
#
#
# async def get_current_user(
#     security_scopes: SecurityScopes, token: Union[str, Depends(oauth2_scheme)], db:AsyncSession
# ):
#     if security_scopes.scopes:
#         authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
#     else:
#         authenticate_value = "Al portador"
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="No se pudieron validar las credenciales",
#         headers={"WWW-Authenticate": authenticate_value},
#     )
#     try:
#         payload = jwt.decode(token, KEY_TOKEN, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_scopes = payload.get("ámbitos", [])
#         token_data = TokenData(scopes=token_scopes, username=username)
#     except (InvalidTokenError, ValidationError):
#         raise credentials_exception
#     user = User.get_user(db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     for scope in security_scopes.scopes:
#         if scope not in token_data.scopes:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="No hay suficientes permisos",
#                 headers={"WWW-Authenticate": authenticate_value},
#             )
#     return user
#
#
# async def get_current_active_user(
#     current_user: Union[User, Security(get_current_user, scopes=["me"])],
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Usuario inactivo")
#     return current_user
