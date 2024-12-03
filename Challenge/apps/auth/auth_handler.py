# import logging
# from datetime import timedelta
# from http.client import HTTPException
# from typing import Union
#
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from passlib.context import CryptContext
#
# from apps.config import APP_NAME, URL_PREFIX, allowed_origins, allow_origin_regex
# from fastapi import FastAPI, Request, status, Depends
# from fastapi.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware import Middleware
# from fastapi.openapi.docs import (get_redoc_html, get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html)
# from fastapi.staticfiles import StaticFiles
#
# # from .auth.authentication import authenticate_user
# from ..auth.token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
# from ..db.models.user import User
# from ..db.schemas.token import Token
# from ..db.db import init_db, get_db
# from sqlalchemy.ext.asyncio import AsyncSession
#
# _logger = logging.getLogger(__name__)
#
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
# app = FastAPI(title=APP_NAME)
# # authentication events
# @app.post("/token")
# async def login_for_access_token(form_data: Union[OAuth2PasswordRequestForm, Depends()],
#                                  db: AsyncSession = Depends(get_db)) -> Token:
#     user = User.authenticate_user(form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username, "scopes": form_data.scopes},
#         expires_delta=access_token_expires,
#     )
#     return Token(access_token=access_token, token_type="bearer")
#
#
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)
#
#
# def get_password_hash(password):
#     return pwd_context.hash(password)
