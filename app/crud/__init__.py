# app/crud/__init__.py
# This file makes the 'crud' directory a Python package
# and is used to expose specific modules or functions from within the package.

# Import specific CRUD modules to make them accessible directly via 'crud.module_name'
from . import user
from . import user_types

# You can also import specific functions/classes if you want them directly under 'crud.'
# For example:
# from .user import get_user, create_user
# from .user_types import get_user_type_option, create_user_type_option
