from decouple import config

APP_NAME = 'Challenge Apirestfull'

HOST ="127.0.0.1" #config('HOST')
PORT = 8070#config('PORT', cast=int)

URL_PREFIX = '/challenge'

allowed_origins = [
    f"http://{HOST}",
    f"http://{HOST}:{PORT}",
   
]

allow_origin_regex = ".*" #config('allow_origin_regex')

# DB
DB_HOST = 'localhost'
DB_PORT = 5432
DB_USER = 'postgres'
DB_PASSWORD = '123qweasd'
DB_NAME = 'challenge'
DB_SCHEMA = "apiRestfull"
