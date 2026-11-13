"""Lazy third-party dependency loading + environment diagnostics.

The web application must boot even when an optional analytics dependency is not
installed. Every pipeline module therefore imports heavy libraries through
:func:`require` at call time, and missing packages surface as a readable
:class:`MissingDependency` message instead of an ``ImportError`` at startup.

A message such as ``pandas is not available`` is useless on its own: it does not
say *which* interpreter is broken. The most common real-world cause is running
the app from an environment that only has ``reflex`` installed (for example
``uv init && uv add reflex``), while the data-science stack lives somewhere
else. Every error raised here therefore names the exact interpreter and the
exact command that fixes it, and :func:`diagnostics` can be rendered in the UI
to make the whole environment auditable at a glance.
"""
from __future__ import annotations

import importlib
import sys
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
    "seaborn": ("seaborn", "Seaborn", "pip install seaborn"),
    "openpyxl": ("openpyxl", "openpyxl", "pip install openpyxl"),
}

# Grouping used by the diagnostics panel so the report reads like a checklist.
TIERS: dict[str, tuple[str, ...]] = {
    "Core data": ("numpy", "pandas", "openpyxl"),
    "Statistics": ("scipy", "statsmodels"),
    "Machine learning": ("sklearn", "joblib"),
    "Data mining": ("duckdb", "polars", "mlxtend"),
    "Optional extras": ("xgboost", "lightgbm", "matplotlib", "seaborn"),
}

# Tiers that must be importable for the full feature set to work.
REQUIRED_TIERS = ("Core data", "Statistics", "Machine learning", "Data mining")

DETAIL_LIMIT = 160


def _exe() -> str:
    """The interpreter currently running the backend, quoted for copy/paste."""
    executable = sys.executable or "python"
    return f'"{executable}"' if " " in executable else executable


def _short(detail: str) -> str:
    text = " ".join(str(detail or "").split())
    return text if len(text) <= DETAIL_LIMIT else text[: DETAIL_LIMIT - 1] + "…"


def install_command(module: str, *, force: bool = False) -> str:
    """Copy-pasteable command that installs ``module`` for *this* interpreter."""
    _, _, install = CATALOG.get(module, (module, module, f"pip install {module.split('.')[0]}"))
    packages = install[len("pip install ") :] if install.startswith("pip install ") else install
    flag = " --force-reinstall" if force else ""
    return f"{_exe()} -m pip install{flag} {packages}"


def requirements_command() -> str:
    """Install every dependency the app expects, for this interpreter."""
    return f"{_exe()} -m pip install -r reflexsqlite/requirements.txt"


def warning(modules: "tuple[str, ...] | list[str]") -> str:
    """One-line, actionable warning when required modules are unavailable.

    Used by page-level preflight banners so a missing library is reported before
    the user clicks Run instead of after the job fails. Metadata-only on
    purpose: this is evaluated on every render, so it must stay cheap.
    """
    missing = [module for module in modules if not is_available(module)]
    if not missing:
        return ""
    labels = ", ".join(CATALOG.get(module, (module, module, ""))[1] for module in missing)
    return (
        f"Missing dependencies: {labels}. Install them for this interpreter "
        f"({_exe()}) with `{requirements_command()}` and restart the app."
    )


class MissingDependency(RuntimeError):
    """Raised when an optional analytics library is needed but unavailable."""

    def __init__(
        self,
        library: str,
        install: str,
        detail: str = "",
        *,
        status: str = "missing",
    ):
        self.library = library
        self.install = install
        self.detail = detail
        # "missing" -> distribution absent; "broken" -> installed but import fails.
        self.status = status
        if status == "broken":
            message = (
                f"{library} is installed but cannot be imported in this environment "
                f"({_short(detail) or 'import failed'}). "
                f"Reinstall it with `{install}` and restart the app."
            )
        else:
            message = f"{library} is not installed. Run `{install}` and restart the app."
        super().__init__(message)


def require(module: str, *, label: str | None = None) -> Any:
    """Import and return ``module`` or raise a friendly :class:`MissingDependency`."""
    distribution, default_label, install = CATALOG.get(
        module, (module.split(".")[0], module, f"pip install {module.split('.')[0]}")
    )
    try:
        return importlib.import_module(module)
    except ImportError as exc:  # includes blocked/broken optional extensions
        # Distinguish "never installed" from "installed but unusable" (blocked
        # DLL, numpy ABI mismatch, half-finished uninstall, ...). The two need
        # very different fixes, so the message must not blur them together.
        broken = is_available(module)
        raise MissingDependency(
            label or default_label,
            install_command(module, force=broken),
            str(exc),
            status="broken" if broken else "missing",
        ) from exc


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


# --------------------------------------------------------------------------- #
# Diagnostics
# --------------------------------------------------------------------------- #


def probe(module: str) -> dict[str, Any]:
    """Actually import ``module`` and report the real outcome.

    Metadata alone is not enough: a package can be registered in
    ``site-packages`` and still fail to import (blocked DLL, broken build).
    Only a real import tells the truth.
    """
    distribution, label, _ = CATALOG.get(module, (module, module, ""))
    record: dict[str, Any] = {
        "module": module,
        "label": label,
        "installed": is_available(module),
        "version": installed_version(module),
        "importable": False,
        "status": "missing",
        "error": "",
        "fix": install_command(module),
    }
    try:
        importlib.import_module(module)
        record["importable"] = True
        record["status"] = "ok"
        record["fix"] = ""
    except ImportError as exc:
        record["error"] = _short(exc)
        if record["installed"]:
            record["status"] = "broken"
            record["fix"] = install_command(module, force=True)
    except Exception as exc:  # noqa: BLE001 - a broken package can raise anything
        record["error"] = f"{type(exc).__name__}: {_short(exc)}"
        record["status"] = "broken"
        record["fix"] = install_command(module, force=True)
    return record


def diagnostics(*, probe_imports: bool = True) -> dict[str, Any]:
    """Full environment report: interpreter, per-library status, next action."""
    packages = {
        module: (probe(module) if probe_imports else {
            "module": module,
            "label": meta[1],
            "installed": is_available(module),
            "version": installed_version(module),
            "importable": False,
            "status": "unknown",
            "error": "",
            "fix": "",
        })
        for module, meta in CATALOG.items()
    }

    groups = []
    for tier, modules in TIERS.items():
        rows = [packages[m] for m in modules if m in packages]
        groups.append(
            {
                "tier": tier,
                "required": tier in REQUIRED_TIERS,
                "rows": rows,
                "ok": all(row["status"] == "ok" for row in rows),
            }
        )

    blocking = [
        row
        for group in groups
        if group["required"]
        for row in group["rows"]
        if row["status"] != "ok"
    ]
    missing = [row["module"] for row in blocking if row["status"] == "missing"]
    broken = [row["module"] for row in blocking if row["status"] == "broken"]

    return {
        "python": {
            "executable": sys.executable,
            "version": ".".join(str(part) for part in sys.version_info[:3]),
            "prefix": sys.prefix,
            "base_prefix": getattr(sys, "base_prefix", sys.prefix),
            "virtual_env": getattr(sys, "prefix", "") != getattr(sys, "base_prefix", ""),
        },
        "groups": groups,
        "packages": packages,
        "missing": missing,
        "broken": broken,
        "ready": not blocking,
        "fix": requirements_command() if blocking else "",
    }
