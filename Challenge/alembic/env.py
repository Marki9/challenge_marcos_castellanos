from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from apps.db.db import Base
from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config


if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base



def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode. """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.url",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(context.configure(
            connection=connection, target_metadata=target_metadata
        ))
        async with connection.begin(): 
            await context.run_migrations()


# Ejecutar las migraciones dependiendo del modo
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
