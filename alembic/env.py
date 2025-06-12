from __future__ import with_statement
import logging
from logging.config import fileConfig
import os # Import os to access environment variables
from dotenv import load_dotenv # Added: For loading environment variables from .env
import sys # Import sys to modify system path
from pathlib import Path # NEW: Import Path for robust path manipulation

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# This is the 'target_metadata' variable from your model's Base.
# It will typically be Base.metadata.

# BEGIN CUSTOM SECTION - MODIFIED FOR NEW PROJECT STRUCTURE
# Add the project root to sys.path to allow absolute imports from 'app'.
# Assuming env.py is inside the 'alembic' directory, two levels up is the project root.
project_root = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(project_root)) # Insert at the beginning for highest priority

# Import Base from your database setup (e.g., app/database.py)
# Now use the absolute import path from the project root
from app.database import Base

# Import all your model modules so that Base.metadata can discover them.
# Even if not directly used here, importing ensures they are registered with Base.metadata.
# Use the absolute import path from the project root
import app.models.user # Corrected import for app/models/user.py

target_metadata = Base.metadata
# END CUSTOM SECTION


# this is the Alembic Config object, which provides
# access to values within the .ini file in use.
config = context.config

# Custom additions for DATABASE URL HANDLING - As per Guzzy's instructions
# Load environment variables from .env file immediately after config is defined
load_dotenv()
# Set the sqlalchemy.url option dynamically from the DATABASE_URL environment variable
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Modified: Get URL from config, which is now set by load_dotenv and os.getenv
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Modified: Removed url=DB_URL as it's now set in config.set_main_option
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        context.run_migrations()

# Interpret the config file for Python's logging module.
# This line was originally at the top, moved here for proper config access.
fileConfig(config.config_file_name)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()