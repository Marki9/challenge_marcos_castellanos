__version__ = "1.0.0"

import logging
from datetime import timedelta
from http.client import HTTPException
from typing import Union

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from apps.config import APP_NAME, URL_PREFIX, allowed_origins, allow_origin_regex
from fastapi import FastAPI, Request, status, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from fastapi.openapi.docs import (get_redoc_html, get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html)
from fastapi.staticfiles import StaticFiles

# # from .auth.authentication import authenticate_user
# from .auth.token import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from .db.models.user import User
from .db.schemas.token import Token
from .routes.users import router as UserRouter
from .routes.posts import router as PostRouter
from .routes.tags import router as TagsRouter
from .db.db import init_db, get_db
from sqlalchemy.ext.asyncio import AsyncSession

from .utils.exceptions import CustomException
from .middleware import ResponseTimeMiddleware

_logger = logging.getLogger(__name__)

app = FastAPI(title=APP_NAME)

app.add_middleware(ResponseTimeMiddleware)

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
# oauth2_scheme = OAuth2PasswordBearer(
#     tokenUrl="token",
#     scopes={"me": "Lee información sobre el usuario actual.", "items": "Leer elementos"},
# )

app.include_router(UserRouter, prefix=URL_PREFIX + "/Users", tags=["Usurarios"])
app.include_router(PostRouter, prefix=URL_PREFIX + "/Posts", tags=["Publicaciones"])
app.include_router(TagsRouter, prefix=URL_PREFIX + "/tags", tags=["Comentarios"])


# Server events
@app.on_event('startup')
async def on_start():
    _logger.info('INFO:    !!Starting Service!!')
    init_db()


@app.on_event('shutdown')
def shutdown():
    _logger.warning('Warning:    !!Service stopped!!')
