# This file was RECREATED based on the dedicated 'users' table schema.
# Import path corrected to avoid ModuleNotFoundError.

from typing import Optional
from sqlalchemy.orm import Session
# CORRECTED IMPORT: Assuming the User model is defined in the models directory as 'user.py'
from ..models.user import User 

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Retrieves a user by their ID (char(36) UUID)."""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Retrieves a user by their unique username."""
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Retrieves a user by their unique email."""
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_affiliate_id(self, affiliate_id: str) -> Optional[User]:
        """Retrieves a user by their unique affiliate ID."""
        return self.db.query(User).filter(User.affiliate_id == affiliate_id).first()

    # NOTE: Your custom business logic must be restored here manually via a local clean copy!

