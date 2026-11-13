"""DataForge - Reflex + SQLite dataset studio.

Entry point used by `reflex run`: the CLI loads `rxconfig.py`, then imports
`<app_name>.<app_name>.py`, so this module is also re-exported at package root.
"""
from __future__ import annotations

import reflex as rx

from .config import settings
from .db import init_db
from .pages import (
    dashboard,
    datasets,
    explore,
    landing,
    login_page,
    mining,
    models,
    register_page,
    settings_page,
    statistics,
)
from .services import dataset_service
from .state import (
    AuthState,
    DashboardState,
    DatasetState,
    ExploreState,
    MiningState,
    ModelsState,
    SettingsState,
    StatisticsState,
)

# Fail-fast bootstrap: schema first, then demo content on an empty database.
init_db()
if settings.seed_demo_data:
    dataset_service.seed_demo()


def _warm_ml_registry() -> None:
    """Load the active .joblib model once at backend startup.

    Wrapped defensively: a missing artifact or an absent optional dependency
    must never stop the web app from booting.
    """
    try:
        from ml_pipelines.inference import warm_start

        warm_start()
    except Exception:  # pragma: no cover - startup resilience
        pass


_warm_ml_registry()

app = rx.App(
    style={
        "font_family": "'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif",
        "background_color": "#F5F7FB",
        "color": "#111827",
    },
)

app.add_page(landing, route="/", title="DataForge · Dataset Studio")
app.add_page(login_page, route="/login", title="Sign in · DataForge", on_load=AuthState.restore)
app.add_page(register_page, route="/register", title="Register · DataForge", on_load=AuthState.restore)
app.add_page(
    dashboard,
    route="/dashboard",
    title="Dashboard · DataForge",
    on_load=[AuthState.require_auth, DashboardState.load_dashboard, DashboardState.live_loop],
)
app.add_page(
    datasets,
    route="/datasets",
    title="Datasets · DataForge",
    on_load=[AuthState.require_auth, DatasetState.load_page],
)
app.add_page(
    explore,
    route="/explore",
    title="Library Workbench · DataForge",
    on_load=[AuthState.require_auth, ExploreState.load_page],
)
app.add_page(
    statistics,
    route="/statistics",
    title="Statistical Profiling · DataForge",
    on_load=[AuthState.require_auth, StatisticsState.load_page],
)
app.add_page(
    models,
    route="/models",
    title="Predictive Models · DataForge",
    on_load=[AuthState.require_auth, ModelsState.load_page],
)
app.add_page(
    mining,
    route="/mining",
    title="Data Mining · DataForge",
    on_load=[AuthState.require_auth, MiningState.load_page],
)
app.add_page(
    settings_page,
    route="/settings",
    title="Settings · DataForge",
    on_load=[AuthState.require_auth, SettingsState.load_settings],
)
