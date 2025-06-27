from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from flask import current_app

import os
import sys

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from src.database import Base
from src.models import User, Post # Import your models here

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired a number of ways:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an actual DBAPI connection.  By doing this,
    migrations can be run without a database connection, however
    skip functions that require a connection such as autogenerate()
    """
    url = config.get_main_option("sqlalchemy.url")
    if url is None:
        # Fallback to Flask app config if no URL in alembic.ini (e.g. for testing)
        try:
            # We explicitly import current_app here to avoid circular imports
            # if flask is not running in the same process as Alembic directly.
            from flask import current_app
            url = current_app.config.get("SQLALCHEMY_DATABASE_URI")
        except RuntimeError:
            # This happens if not in a Flask app context, which is fine for offline
            # as long as URL is provided via alembic.ini or defaults to a dummy one.
            pass # Keep url as None or use a placeholder if necessary

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"use_alter": True} # Important for SQLite's ALTER TABLE support
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.", # Important: prefix for sqlalchemy options in alembic.ini
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True, # Required for SQLite to correctly handle ALTER operations
            dialect_opts={"use_alter": True} # Important for SQLite's ALTER TABLE support
        )

        with context.begin_transaction(): # Ensure transaction for online migrations too
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
