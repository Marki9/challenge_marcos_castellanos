from decouple import config
import logging

APP_NAME = 'Challenge Apirestfull'

HOST ="127.0.0.1" #config('HOST')
PORT = 8070#config('PORT', cast=int)

URL_PREFIX = '/challenge'

# DB
DB_HOST = 'localhost'
DB_PORT = 5432
DB_USER = 'postgres'
DB_PASSWORD = '123qweasd'
DB_NAME = 'challenge'
DB_SCHEMA = "apiRestfull"

logger = logging.getLogger("uvicorn.error")