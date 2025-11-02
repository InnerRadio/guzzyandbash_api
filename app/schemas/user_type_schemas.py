# app/schemas/user_type_schemas.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserTypeOptionBase(BaseModel):
    name: str = Field(..., example="Creator", description="Name of the user type option")
    description: Optional[str] = Field(None, example="User who creates content and earns royalties", description="Description of the user type option")
    is_active: bool = Field(True, description="Whether the user type option is active")

class UserTypeOptionCreate(UserTypeOptionBase):
    """Schema for creating a new UserTypeOption."""
    pass

class UserTypeOptionUpdate(UserTypeOptionBase):
    """Schema for updating an existing UserTypeOption. All fields are optional for updates."""
    name: Optional[str] = Field(None, example="Creator", description="Name of the user type option")
    is_active: Optional[bool] = Field(None, description="Whether the user type option is active")

class UserTypeOptionResponse(UserTypeOptionBase):
    """Schema for returning a UserTypeOption from the API."""
    id: str = Field(..., example="uuid_string", description="Unique identifier for the user type option")
    created_at: datetime = Field(..., description="Timestamp when the user type option was created")
    last_updated_at: datetime = Field(..., description="Timestamp when the user type option was last updated")

    class Config:
        from_attributes = True # Pydantic v2 equivalent of orm_mode = True
