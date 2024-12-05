from datetime import timedelta

import jwt
from fastapi import Depends, HTTPException, Security, status, APIRouter
from fastapi.security import (
    OAuth2PasswordRequestForm, SecurityScopes,
)

from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from apps.auth.auth_handler import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, verify_password, SECRET_KEY, ALGORITHM
from apps.db.db import get_db
from apps.db.schemas.token import Token, TokenData
from apps.db.schemas.user import UserResponse, User
from apps.db.models.user import User as UserM

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Leer información del usuario.", "items": "Read items."},
)

router= APIRouter()


def get_user(username: str, db: Session = Depends(get_db)):
    result = db.query(UserM).filter(UserM.username == username).first()
    if result:
        return result


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = get_user(username=username, db=db)
    if not user:
        return False
    if not verify_password(password=password, hashed_password=user.password):
        return False
    return user


async def get_current_user(
        security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pueden validar sus credenciales",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (InvalidTokenError, ValidationError):
        raise credentials_exception
    user = get_user(token_data.username, db)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No tiene permisos suficientes",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(
        current_user: User = Security(get_current_user, scopes=["me"]),
):

    return current_user


@router.post("/token",include_in_schema=False)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrecta")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/", response_model=UserResponse,include_in_schema=False)
async def read_users_me(
        current_user: User = Depends(get_current_active_user)):
    a=[current_user]

    return UserResponse(a, True, 1, '')


