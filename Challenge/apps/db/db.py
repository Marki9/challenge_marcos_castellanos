import logging
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import text
from sqlalchemy.schema import CreateSchema
from sqlalchemy_utils import create_database, database_exists, drop_database
from sqlalchemy import pool
from alembic import context
from ..config import DB_HOST, DB_PASSWORD, DB_NAME, DB_PORT, DB_USER, DB_SCHEMA

logging.basicConfig(level=logging.INFO, format="%(message)s >> %(asctime)s", datefmt="%d/%m/%Y %H:%M:%S")
_logger = logging.getLogger(__name__)

PG_DATABASE_URL = 'postgresql+psycopg2://%s:%s@%s:%s/%s' % (DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
ASYNC_PG_DATABASE_URL = 'postgresql+asyncpg://%s:%s@%s:%s/%s' % (DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
engine = create_engine(PG_DATABASE_URL)
async_engine = create_async_engine(ASYNC_PG_DATABASE_URL)
SessionFactory = sessionmaker(bind=engine, autoflush=False)
AsyncSessionFactory = sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)

metadat = MetaData(schema=DB_SCHEMA)

# Crear una clase base para los modelos
Base = declarative_base(metadata=metadat)


# Base = declarative_base()


# Dependencia para obtener la sesión de la base de datos
async def get_db_Async():
    async with AsyncSessionFactory() as db:
        yield db


def get_db():
    try:
        db = SessionFactory()
        yield db
    finally:
        db.close()


def create_db():
    try:
        _logger.info(f"INFO:    !!Conecting to PostgresSQL server at '127.0.0.1:8000' with user: 'postgres'!!")
        if not database_exists(engine.url):
            _logger.info(f"INFO:    !!Creating DB 'challenge' with SQLAlchemy!!")
            create_database(engine.url)
        _logger.info(f"INFO:    *** Successful conecction with DB 'challenge' ***")
    except Exception as e:
        raise e


def init_db():
    try:
        create_db()
        # Crear el esquema si no existe
        with engine.connect() as connection:
            if not connection.dialect.has_schema(connection, DB_SCHEMA):
                _logger.info(f"Intentando crear el esquema: {DB_SCHEMA}")
                connection.execute(CreateSchema(DB_SCHEMA, if_not_exists=False))
                connection.commit()

        # Crea todas las tablas en la base de datos
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        _logger.error(e)
        raise e


async def init_db_Async():
    try:
        create_db()
        # Crear el esquema si no existe
        async with async_engine.connect() as connection:
            query = text(f"SELECT EXISTS (SELECT 1 FROM information_schema.schemata WHERE schema_name = :schema_name)")
            exists = await connection.scalar(query, {"schema_name": DB_SCHEMA})
            if not exists:
                _logger.info(f"Intentando crear el esquema: {DB_SCHEMA}")
                await connection.execute(CreateSchema(DB_SCHEMA, if_not_exists=False))
                await connection.commit()
        # Crea todas las tablas en la base de datos
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        _logger.error(e)
        raise e


def drop_db():
    drop_database(engine.url)


def checkConnection():
    try:
        engine.execute(text("SELECT 1"))
        return True
    except SQLAlchemyError as e:
        _logger.error(e)
        return False
    except Exception as e:
        _logger.error(e)
        return False
