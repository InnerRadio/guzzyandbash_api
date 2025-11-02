# app/core/config.py
# This file defines the application's configuration settings using Pydantic's BaseSettings.
# BaseSettings allows loading settings from environment variables, .env files,
# and provides validation, making configuration management robust and secure.

# Pydantic imports for BaseSettings and field validation
from pydantic_settings import BaseSettings, SettingsConfigDict # For defining settings and configuration
from pydantic import Field # For defining field properties like min_length

# --- Application Settings Class ---
# This class defines all the configuration variables for your FastAPI application.
# Pydantic's BaseSettings automatically reads environment variables that match
# the field names (case-insensitive by default, but can be configured).
class Settings(BaseSettings):
    # model_config provides configuration for the Pydantic model itself.
    # It specifies that settings should be read from a .env file.
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # --- Database Settings ---
    # These settings are crucial for connecting to your PostgreSQL database.
    # They are loaded from environment variables (e.g., DATABASE_URL in .env).
    DATABASE_URL: str = Field(
        ..., # Ellipsis indicates this field is required
        description="The URL for connecting to the PostgreSQL database (e.g., 'postgresql+psycopg2://user:password@host:port/dbname')."
    )

    # --- JWT Authentication Settings ---
    SECRET_KEY: str = Field(
        ...,
        min_length=32, # Ensure the key is sufficiently long for security
        description="A secret key used for encoding JWT tokens. **CRITICAL: Keep this confidential and generate a strong, random one!**"
    )
    ALGORITHM: str = Field(
        "HS256", # Common algorithm for JWT
        description="The hashing algorithm used for JWT token signing."
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        30, # Access token validity period in minutes
        description="The lifespan of access tokens in minutes."
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        7, # Refresh token validity period in days
        description="The lifespan of refresh tokens in days."
    )

    # --- XRPL Settings ---
    XRPL_NETWORK_URL: str = Field(
        ...,
        description="The URL of the XRPL network (e.g., Testnet, Mainnet RPC endpoint)."
    )
    XRPL_WALLET_SEED: str = Field(
        ..., # Ellipsis indicates this field is required
        description="The secret seed for the Guzzy & Bash Productions XRPL wallet. **CRITICAL: KEEP THIS CONFIDENTIAL!**"
    )

    # --- Other Application Settings (Examples) ---
    # You can add any other application-specific settings here.
    # For example, settings for external APIs, logging levels, etc.
    APP_NAME: str = Field(
        "Guzzy & Bash Productions API",
        description="The name of your FastAPI application."
    )
    DEBUG_MODE: bool = Field(
        False, # Set to True for development, False for production
        description="Enable or disable debug mode for the application."
    )
    # NEW: Add ENVIRONMENT field
    ENVIRONMENT: str = Field(
        "development", # Default value, can be overridden by .env
        description="The application's environment (e.g., 'development', 'production', 'testing')."
    )
    # Example for a placeholder image service URL
    PLACEHOLDER_IMAGE_SERVICE_URL: str = Field(
        "https://placehold.co",
        description="URL for a placeholder image service (e.g., for default profile pictures)."
    )
    # Example for a default profile picture URL
    DEFAULT_PROFILE_PICTURE_URL: str = Field(
        "https://placehold.co/150x150/aabbcc/ffffff?text=User",
        description="Default URL for user profile pictures."
    )

# Create an instance of the Settings class.
# This instance will automatically load settings from environment variables
# and the .env file as configured in model_config.
settings = Settings()