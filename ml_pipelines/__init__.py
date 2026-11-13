"""DataForge ML pipelines.

This package is intentionally *independent of Reflex*. It contains all data
preprocessing, statistical modelling, training, inference and large-scale
mining code. The web application (``reflexsqlite/reflexsqlite/``) only consumes
plain dictionaries and lists returned from here, so every pipeline can also be
run from the command line::

    python -m ml_pipelines --help
    python -m ml_pipelines train --dataset-id 1 --target revenue

Nothing heavy is imported at package import time: :mod:`ml_pipelines._optional`
loads third-party libraries lazily so the web app still boots when an optional
dependency (xgboost, lightgbm, duckdb, ...) is missing.
"""
from __future__ import annotations

from ._optional import (  # noqa: F401
    MissingDependency,
    availability,
    diagnostics,
    install_command,
    probe,
    require,
    requirements_command,
)
from .paths import (  # noqa: F401
    database_path,
    ensure_model_dir,
    models_dir,
    uploads_dir,
    workspace_root,
)

__all__ = [
    "MissingDependency",
    "availability",
    "diagnostics",
    "install_command",
    "probe",
    "require",
    "requirements_command",
    "workspace_root",
    "database_path",
    "models_dir",
    "uploads_dir",
    "ensure_model_dir",
    "__version__",
]

__version__ = "1.0.0"
