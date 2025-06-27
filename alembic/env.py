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
# Use the absolute import path from the project root.
# Based on your app/models/ directory listing:
import app.models.user
import app.models.affiliate # Added for AffiliateClick model
import app.models.nft       # Added for MintedMemorialEntry model
# If you have a specific 'Post' model in app/models/post.py, uncomment/add:
# import app.models.post

target_metadata = Base.metadata
# END CUSTOM SECTION


# this is the Alembic Config object, which provides
# access to values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
# CORRECTED: Use config.config_file_name for the path to the .ini file.
fileConfig(config.config_file_name)


# Custom additions for DATABASE URL HANDLING - As per Guzzy's instructions
# Load environment variables from .env file immediately after config is defined
# IMPORTANT: Use override=True here to ensure .env values take precedence
# over any existing shell environment variables (e.g., the "$(DATABASE_URL)" issue)
load_dotenv(override=True)
# Set the sqlalchemy.url option dynamically from the DATABASE_URL environment variable
db_url_from_env = os.getenv("DATABASE_URL")
if db_url_from_env:
    config.set_main_option("sqlalchemy.url", db_url_from_env)
    # TEMPORARY DEBUG PRINT: Confirm the URL being set
    print(f"DEBUG (env.py): Setting Alembic config URL to: {db_url_from_env}", file=sys.stderr)
else:
    print("WARNING (env.py): DATABASE_URL not found in .env file. Alembic might fail to connect.", file=sys.stderr)


def run_migrations_offline() -> None:
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
    if not url: # Safety check
        print("CRITICAL ERROR (Offline): Database URL is not set for offline migration.", file=sys.stderr)
        return

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    # The URL should already be set in config.set_main_option by the top-level code.
    # We retrieve it here to pass to engine_from_config.
    db_url = config.get_main_option("sqlalchemy.url")
    if not db_url:
        raise Exception("CRITICAL ERROR (Online): DATABASE_URL is not set. "
                        "Please ensure DATABASE_URL is in your .env file and correctly loaded.")

    # TEMPORARY DEBUG PRINT:
    print(f"DEBUG (Online): Using DB URL from config: {db_url}", file=sys.stderr)

    connectable = engine_from_config(
        {"sqlalchemy.url": db_url}, # Pass the URL found directly
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # Add this if you face issues with UUID columns and MariaDB/MySQL connector
            # You might need to remove this or adjust if your database schema for UUIDs is strict binary
            # version_table_pk_exists=False # This might be needed for certain MariaDB/MySQL versions or UUID setups.
        )

        with context.begin_transaction():
            # The time.sleep(1) was present in your previous env.py from GitHub.
            # While generally not needed for migrations, if you've found it helpful
            # in your environment for "reloading" or caching issues, keep it.
            # Otherwise, it can be removed.
            # For now, keeping it as it was in your working GitHub version.
            # time.sleep(1) # Sleep for 1 second (Removed as it's typically unnecessary and slows down)
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

