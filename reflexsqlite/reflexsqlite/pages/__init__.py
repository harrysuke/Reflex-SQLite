"""Page components."""
from .auth import login_page, register_page
from .dashboard import dashboard
from .datasets import datasets
from .explore import explore
from .landing import landing
from .mining import mining
from .models import models
from .settings import settings_page
from .statistics import statistics

__all__ = [
    "landing",
    "login_page",
    "register_page",
    "dashboard",
    "datasets",
    "explore",
    "mining",
    "models",
    "settings_page",
    "statistics",
]
