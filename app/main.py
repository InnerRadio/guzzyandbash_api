# app/main.py
# This file is the main entry point for the FastAPI application.
# It sets up the application, includes routers, and defines event handlers.
import sys
import asyncio
import os # Standard library import for operating system interactions
from pathlib import Path
from datetime import timedelta
import logging
# NEW: Import settings from the new config module
from app.core.config import settings # CORRECTED IMPORT PATH
# Add the project root to the sys.path for absolute imports
# This ensures that imports like 'from app.database import engine' work correctly
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))
# Configure logging for the entire application
# CRITICAL CHANGE: Set the root logger level to DEBUG to capture all messages
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# Log sys.path and current working directory for debugging
logger.debug(f"main.py before controller imports - sys.path: {sys.path}")
logger.debug(f"main.py before controller imports - os.getcwd(): {os.getcwd()}")
# REMOVED: dotenv import and load_dotenv call - settings are now loaded via app.core.config
# from dotenv import load_dotenv
# load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
# Debugging: Print the SECRET_KEY directly at startup
# Now from the settings object - USE settings.SECRET_KEY
# NOTE: In a production environment, avoid printing sensitive information directly.
logger.debug(f"FastAPI app starting with environment: {settings.ENVIRONMENT}")
# logger.debug(f"FastAPI app using SECRET_KEY: {settings.SECRET_KEY[:5]}...") # Log first 5 chars for debug
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import SessionLocal # Import SessionLocal for middleware
from starlette.middleware.base import BaseHTTPMiddleware # For database session middleware
# Import the base for SQLAlchemy declarative models
# This import ensures that all models are registered with SQLAlchemy's metadata
from app.database import Base # This is crucial for init_db()
# NEW: Import SQLAlchemy model *modules* for model_rebuild's _types_namespace
# This helps ensure models are fully loaded before schemas are rebuilt
import app.models.nft # Import the module
# Removed 'import app.models.user' because it caused a duplicate table error
import app.models.content # Import the module for Content relationships
import app.models.activity_log # Import the module for ActivityLog relationships
# NEW: Import Pydantic schemas for model_rebuild
from app.schemas.user_schemas import UserResponse, NFTResponse, UserFullProfile
# Application-specific imports (routers, dependencies, database)
from app.database import get_db, init_db # Database session and initialization
from app.dependencies import get_current_user # Dependency for authentication
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials # Correct import for Bearer Token security
# Import controllers for API endpoints
from app.controllers import (
    auth as auth_router, # Authentication routes
    user as user_router, # NEW LINE: Core user management routes (e.g., /me, /profile)
    user_types as user_types_router, # User type related routes (e.g., roles)
    admin_reports as admin_reports_router, # Admin-specific reports
    public_reports as public_reports_router, # Publicly accessible reports
    nft_operations as nft_operations_router, # NFT minting and related operations
    user_reports as user_reports_router, # User-specific reports
    affiliate_reports as affiliate_reports_router # Affiliate program reports
)
# Remove nest_asyncio if uvloop is not installed
# This is a common fix if you encounter RuntimeError: 'This event loop is already running'
# when trying to run multiple asyncio loops (e.g., in Jupyter notebooks or some testing setups)
try:
    import uvloop
    # If uvloop is installed, FastAPI will likely use it. No need for nest_asyncio.
    logger.debug("uvloop detected. Not applying nest_asyncio.")
except ImportError:
    # If uvloop is not installed, nest_asyncio might be needed in certain environments.
    # However, for typical FastAPI deployments, it's often not necessary and can cause issues.
    # We remove it as per the project's refactoring notes.
    # import nest_asyncio
    # nest_asyncio.apply() # REMOVED as per refactoring notes.
    logger.debug("uvloop not detected. nest_asyncio.apply() explicitly removed per project notes.")
# Initialize FastAPI application
app = FastAPI(
    title="Guzzy and Bash Productions API",
    description="API for managing users, content, NFTs, and reports.",
    version="0.1.0",
    docs_url="/docs", # Swagger UI
    redoc_url="/redoc", # ReDoc documentation
    openapi_url="/openapi.json", # OpenAPI schema
    swagger_ui_oauth2_redirect_url="/oauth2-redirect", # For OAuth2 in Swagger UI
    swagger_ui_init_oauth={ # Configure OAuth2 for Swagger UI
        "clientId": "your-client-id", # Replace with your actual client ID
        "clientSecret": "your-client-secret", # Replace with your actual client secret if applicable
        "appName": "Guzzy and Bash API"
    }
)
# Add Security Definitions to OpenAPI Schema
# This ensures that the BearerAuth scheme appears in the Swagger UI
# app.add_middleware(BaseHTTPMiddleware, dispatch=HTTPBearer().dispatch)
# CORS Middleware Configuration
# Allows requests from specified origins to prevent CORS errors in browsers
origins = [
    # Allow all origins for development (remove in production)
    "*",
    # "http://localhost:3000", # Example: frontend running on localhost
    # "https://your-production-domain.com", # Example: your production frontend
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allow all HTTP methods
    allow_headers=["*"], # Allow all headers
)
# Database Session Middleware
# This middleware creates a database session for each request and closes it afterwards.
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    """
    Middleware to manage database sessions for each request.
    Ensures a new session is created for each request and properly closed.
    """
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response
# Include API Routers
# These routes define the API endpoints for different functionalities
app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(user_router.router, prefix="/api/v1/user", tags=["User Management"])
app.include_router(user_types_router.router, prefix="/api/v1/user-types", tags=["User Types & Roles"])
app.include_router(admin_reports_router.router, prefix="/api/v1/admin/reports", tags=["Admin Reports"], dependencies=[]) # Add dependencies for admin roles
app.include_router(public_reports_router.router, prefix="/api/v1/reports", tags=["Public Reports"])
app.include_router(nft_operations_router.router, prefix="/api/v1/nft", tags=["NFT Operations"])
app.include_router(user_reports_router.router, prefix="/api/v1/user/reports", tags=["User Reports"])
app.include_router(affiliate_reports_router.router, prefix="/api/v1/affiliate/reports", tags=["Affiliate Reports"])

@app.get("/")
async def read_root():
    """
    Root endpoint of the API.
    Returns a welcome message.
    """
    logger.info("Root endpoint accessed.")
    return {"message": "Welcome to Guzzy and Bash Productions API! Go to /docs for API documentation."}
@app.on_event("startup")
async def startup_event():
    """
    Handles startup events for the application.
    - Initializes the database.
    - Rebuilds Pydantic models.
    """
    logger.debug("Application startup event triggered.")
    logger.debug(f"Current app routes: {len(app.routes)} routes defined.")
    for route in app.routes:
        if hasattr(route, 'path') and hasattr(route, 'methods'):
            logger.debug(f"  - Route: {route.path}, Methods: {route.methods}")
    # Initialize the database (create tables if they don't exist)
    # This ensures your SQLAlchemy models are mapped to database tables on startup.
    if asyncio.iscoroutinefunction(init_db):
        await init_db()
    else:
        init_db()
    logger.debug("SQLAlchemy Base registry configured.")
    logger.debug("Database initialized successfully.")
    # Rebuild Pydantic models
    # This is essential for handling circular dependencies or forward references
    # in your Pydantic schemas, ensuring they are fully resolved after all
    # modules have been loaded.
    # Pass the module's dictionary to _types_namespace for better resolution
    # Use sys.modules to get the already loaded module's namespace
    all_models_namespace = globals() # FIXED: Replaced crashing sys.modules lookup with simple globals()
    try:
        UserResponse.model_rebuild(_types_namespace=all_models_namespace)
        logger.debug("UserResponse.model_rebuild() successful.")
    except Exception as e:
        logger.error(f"UserResponse.model_rebuild() failed: {e}")
        raise
    try:
        NFTResponse.model_rebuild(_types_namespace=all_models_namespace)
        logger.debug("NFTResponse.model_rebuild() successful.")
    except Exception as e:
        logger.error(f"NFTResponse.model_rebuild() failed: {e}")
        raise
    # Rebuild UserFullProfile model as it's a complex schema
    try:
        UserFullProfile.model_rebuild(_types_namespace=all_models_namespace)
        logger.debug("UserFullProfile.model_rebuild() successful.")
    except Exception as e:
        logger.error(f"UserFullProfile.model_rebuild() failed: {e}")
        raise
    logger.debug("Application startup complete.")
@app.on_event("shutdown")
async def shutdown_event():
    """
    Handles shutdown events for the application.
    Placeholder for any cleanup or resource release logic.
    """
    logger.debug("Application shutdown event triggered.")
    logger.debug("Guzzy and Bash Productions API has shut down.")
