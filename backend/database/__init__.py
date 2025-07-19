# backend/database/__init__.py
from .schema import init_db
from .users import get_or_create_user
from .projects import save_project, get_user_projects, load_project
