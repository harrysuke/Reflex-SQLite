"""Lazy third-party dependency loading.

The web application must boot even when an optional analytics dependency is not
installed. Every pipeline module therefore imports heavy libraries through
:func:`require` at call time, and missing packages surface as a readable
:class:`MissingDependency` message instead of an ``ImportError`` at startup.
"""
from __future__ import annotations

import importlib
from importlib.metadata import PackageNotFoundError, version
from typing import Any

# module name -> (pip distribution, human label, install hint)
CATALOG: dict[str, tuple[str, str, str]] = {
    "numpy": ("numpy", "NumPy", "pip install numpy"),
    "pandas": ("pandas", "pandas", "pip install pandas"),
    "scipy": ("scipy", "SciPy", "pip install scipy"),
    "statsmodels": ("statsmodels", "statsmodels", "pip install statsmodels"),
    "sklearn": ("scikit-learn", "scikit-learn", "pip install scikit-learn"),
    "joblib": ("joblib", "joblib", "pip install joblib"),
    "duckdb": ("duckdb", "DuckDB", "pip install duckdb"),
    "polars": ("polars", "Polars", "pip install polars"),
    "mlxtend": ("mlxtend", "mlxtend", "pip install mlxtend"),
    "xgboost": ("xgboost", "XGBoost", "pip install xgboost"),
    "lightgbm": ("lightgbm", "LightGBM", "pip install lightgbm"),
    "matplotlib": ("matplotlib", "Matplotlib", "pip install matplotlib"),
    "openpyxl": ("openpyxl", "openpyxl", "pip install openpyxl"),
}


class MissingDependency(RuntimeError):
    """Raised when an optional analytics library is needed but unavailable."""

    def __init__(self, library: str, install: str, detail: str = ""):
        self.library = library
        self.install = install
        message = f"{library} is not available. Run `{install}` and restart the app."
        if detail:
            message += f" ({detail})"
        super().__init__(message)


def require(module: str, *, label: str | None = None) -> Any:
    """Import and return ``module`` or raise a friendly :class:`MissingDependency`."""
    distribution, default_label, install = CATALOG.get(
        module, (module.split(".")[0], module, f"pip install {module.split('.')[0]}")
    )
    try:
        return importlib.import_module(module)
    except ImportError as exc:  # includes blocked/broken optional extensions
        raise MissingDependency(label or default_label, install, str(exc)) from exc


def is_available(module: str) -> bool:
    """Check installed distribution metadata without importing the module."""
    distribution, _, _ = CATALOG.get(module, (module.split(".")[0], "", ""))
    for candidate in dict.fromkeys((distribution, module.split(".")[0])):
        try:
            version(candidate)
            return True
        except PackageNotFoundError:
            continue
    return False


def installed_version(module: str) -> str:
    distribution, _, _ = CATALOG.get(module, (module.split(".")[0], "", ""))
    for candidate in dict.fromkeys((distribution, module.split(".")[0])):
        try:
            return version(candidate)
        except PackageNotFoundError:
            continue
    return ""


def availability() -> dict[str, dict[str, str | bool]]:
    """Serializable capability report for the UI / CLI."""
    return {
        module: {
            "available": is_available(module),
            "version": installed_version(module),
            "label": meta[1],
            "install": meta[2],
        }
        for module, meta in CATALOG.items()
    }
