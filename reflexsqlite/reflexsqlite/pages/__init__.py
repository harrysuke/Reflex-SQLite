"""Page components."""
from .auth import login_page, register_page
from .dashboard import dashboard
from .datasets import datasets
from .explore import explore
from .landing import landing
from .settings import settings_page

__all__ = [
    "landing",
    "login_page",
    "register_page",
    "dashboard",
    "datasets",
    "explore",
    "settings_page",
]
