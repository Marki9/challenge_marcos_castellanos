__version__ = "1.0.0"

import logging
from apps.config import APP_NAME, URL_PREFIX,allowed_origins,allow_origin_regex
from typing import Type, Optional
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from fastapi.openapi.docs import (get_redoc_html, get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html )
from fastapi.staticfiles import StaticFiles
from .auth.authentication import router as AuthRouter
from .routes.users import router as UserRouter
from .routes.posts import router as PostRouter
from .routes.tags import router as TagsRouter
from .db.db import init_db

from .utils.exceptions import CustomException
from .middleware import ResponseTimeMiddleware

_logger = logging.getLogger(__name__)

app = FastAPI(title=APP_NAME)

app.add_middleware(ResponseTimeMiddleware)

app.include_router(AuthRouter, prefix=URL_PREFIX + "/auth", tags=["Authentication"])
app.include_router(UserRouter, prefix=URL_PREFIX + "/Users", tags=["Usurarios"])
app.include_router(PostRouter, prefix=URL_PREFIX + "/Posts", tags=["Publicaciones"])
app.include_router(TagsRouter, prefix=URL_PREFIX + "/tags", tags=["Comentarios"])

# Server events
@app.on_event('startup')
def on_start():
    _logger.info('INFO:    !!Starting Service!!')
    init_db()


@app.on_event('shutdown')
def shutdown():
    _logger.warning('Warning:    !!Service stopped!!')