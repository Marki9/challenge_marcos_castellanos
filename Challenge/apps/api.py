__version__ = "1.0.0"
import logging
from apps.config import APP_NAME, URL_PREFIX, allowed_origins, allow_origin_regex
from fastapi import FastAPI

from .auth.authentication import router as AuthenticationRouter
from .routes.users import router as UserRouter
from .routes.posts import router as PostRouter
from .routes.tags import router as TagsRouter
from .db.db import init_db, get_db

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
app.include_router(AuthenticationRouter)
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
