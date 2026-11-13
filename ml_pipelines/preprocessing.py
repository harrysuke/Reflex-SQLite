"""Feature preparation shared by training and inference.

The estimator is a single scikit-learn ``Pipeline`` (impute -> scale / one-hot
-> model). Serializing the pipeline together with its feature list guarantees
that inference applies *exactly* the same transformations as training, which is
the most common source of train/serve skew.
"""
from __future__ import annotations

import math
from typing import Any, Sequence

from ._optional import require
from .data_access import RESERVED_PREFIX


def json_safe(value: Any) -> Any:
    """Convert numpy / pandas scalars into JSON-serializable Python values."""
    if value is None:
        return None
    if hasattr(value, "item") and not isinstance(value, (str, bytes, dict, list)):
        try:
            return json_safe(value.item())
        except (ValueError, AttributeError, TypeError):
            pass
    if isinstance(value, bool):
        return bool(value)
    if isinstance(value, int):
        return int(value)
    if isinstance(value, float):
        return None if not math.isfinite(value) else float(value)
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [json_safe(v) for v in value]
    return str(value)


def float_or_none(value: Any) -> float | None:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def clean_frame(frame, drop_reserved: bool = True):
    """Drop internal columns and normalize column names to plain strings."""
    frame = frame.copy()
    frame.columns = [str(c) for c in frame.columns]
    if drop_reserved:
        internal = [c for c in frame.columns if c.startswith(RESERVED_PREFIX)]
        if internal:
            frame = frame.drop(columns=internal)
    return frame


def numeric_columns(frame, candidates: Sequence[str] | None = None, *, threshold: float = 0.9):
    """Detect numeric columns, including object columns holding numeric strings."""
    pd = require("pandas")
    columns = list(candidates) if candidates is not None else list(frame.columns)
    result = []
    for column in columns:
        if column not in frame.columns:
            continue
        series = frame[column]
        if pd.api.types.is_numeric_dtype(series):
            result.append(column)
            continue
        coerced = pd.to_numeric(series, errors="coerce")
        non_null = int(series.notna().sum())
        if non_null and coerced.notna().sum() / non_null >= threshold:
            result.append(column)
    return result


def categorical_columns(frame, numeric: Sequence[str]) -> list[str]:
    return [str(c) for c in frame.columns if c not in set(numeric)]


def infer_task(target, *, regression_unique_threshold: int = 15) -> str:
    """Classification for low-cardinality / non-numeric targets, else regression."""
    pd = require("pandas")
    if not pd.api.types.is_numeric_dtype(target):
        return "classification"
    cleaned = pd.to_numeric(target, errors="coerce").dropna()
    if cleaned.empty or cleaned.nunique() <= regression_unique_threshold:
        return "classification"
    return "regression"


def split_features(frame, target: str, task: str | None = None):
    """Return (X, y, numeric_features, categorical_features, task)."""
    pd = require("pandas")
    if target not in frame.columns:
        raise ValueError(f"Target column '{target}' is not in the dataset.")
    working = clean_frame(frame)
    y = pd.to_numeric(working[target], errors="coerce") if task == "regression" else working[target]
    if task is None:
        task = infer_task(working[target])
        y = pd.to_numeric(working[target], errors="coerce") if task == "regression" else working[target]
    x = working.drop(columns=[target])
    numeric = numeric_columns(x)
    categorical = categorical_columns(x, numeric)
    for column in numeric:
        x[column] = pd.to_numeric(x[column], errors="coerce")
    for column in categorical:
        x[column] = x[column].astype("string").fillna("").astype(str)
    valid = y.notna()
    if task == "regression":
        valid &= pd.to_numeric(y, errors="coerce").notna()
    return x.loc[valid], y.loc[valid], numeric, categorical, task


def build_estimator(task: str, algorithm: str, numeric: Sequence[str], categorical: Sequence[str]):
    """Construct an unfitted scikit-learn Pipeline.

    Supported algorithms: ``random_forest``, ``gradient_boosting``, ``linear``,
    ``xgboost`` and ``lightgbm``. Optional extras (and even ``sklearn.ensemble``
    on locked-down hosts whose application-control policy blocks a compiled
    DLL) degrade gracefully to the next available estimator. The returned
    ``algorithm`` is the one actually used, so callers can report a substitution.
    """
    from sklearn.compose import ColumnTransformer
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LinearRegression, LogisticRegression
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler

    numeric_pipe = Pipeline(
        [
            ("impute", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()),
        ]
    )
    categorical_pipe = Pipeline(
        [
            ("impute", SimpleImputer(strategy="constant", fill_value="")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )
    transformers = []
    if numeric:
        transformers.append(("num", numeric_pipe, list(numeric)))
    if categorical:
        transformers.append(("cat", categorical_pipe, list(categorical)))
    if not transformers:
        raise ValueError("No usable feature columns were found.")
    pre = ColumnTransformer(transformers, remainder="drop")

    classification = task == "classification"

    def _linear():
        return (
            LogisticRegression(max_iter=1000, random_state=42)
            if classification
            else LinearRegression()
        )

    def _forest():
        from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

        return (
            RandomForestClassifier(n_estimators=160, min_samples_leaf=2, random_state=42, n_jobs=-1)
            if classification
            else RandomForestRegressor(n_estimators=160, min_samples_leaf=2, random_state=42, n_jobs=-1)
        )

    def _gradient_boosting():
        from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor

        return (
            GradientBoostingClassifier(random_state=42)
            if classification
            else GradientBoostingRegressor(random_state=42)
        )

    def _tree():
        from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

        return (
            DecisionTreeClassifier(random_state=42)
            if classification
            else DecisionTreeRegressor(random_state=42)
        )

    def _xgboost():
        xgb = require("xgboost")
        common = dict(
            n_estimators=180, max_depth=5, learning_rate=0.08,
            subsample=0.9, colsample_bytree=0.9, random_state=42, n_jobs=4,
        )
        return (
            xgb.XGBClassifier(eval_metric="logloss", verbosity=0, **common)
            if classification
            else xgb.XGBRegressor(verbosity=0, **common)
        )

    def _lightgbm():
        lgb = require("lightgbm")
        common = dict(n_estimators=180, learning_rate=0.08, random_state=42, verbose=-1, n_jobs=4)
        return (
            lgb.LGBMClassifier(**common) if classification else lgb.LGBMRegressor(**common)
        )

    builders = {
        "linear": _linear,
        "random_forest": _forest,
        "gradient_boosting": _gradient_boosting,
        "tree": _tree,
        "xgboost": _xgboost,
        "lightgbm": _lightgbm,
    }
    fallbacks = {
        "xgboost": ["xgboost", "lightgbm", "random_forest", "gradient_boosting", "tree", "linear"],
        "lightgbm": ["lightgbm", "xgboost", "random_forest", "gradient_boosting", "tree", "linear"],
        "gradient_boosting": ["gradient_boosting", "random_forest", "tree", "linear"],
        "random_forest": ["random_forest", "gradient_boosting", "tree", "linear"],
        "linear": ["linear", "random_forest", "tree"],
    }
    order = fallbacks.get(algorithm, ["random_forest", "tree", "linear"])

    last_error: Exception | None = None
    for candidate in order:
        builder = builders.get(candidate)
        if builder is None:
            continue
        try:
            model = builder()
        except Exception as exc:  # ImportError, MissingDependency, blocked DLL, ...
            last_error = exc
            continue
        return Pipeline([("pre", pre), ("model", model)]), candidate

    raise RuntimeError(f"No estimator could be constructed: {last_error}")



def frame_to_records(frame, columns: Sequence[str] | None = None, limit: int = 30) -> list[dict[str, Any]]:
    """Convert a pandas/polars frame into UI-ready string records."""
    if hasattr(frame, "to_dicts"):  # polars
        rows = frame.head(limit).to_dicts()
    else:
        rows = frame.head(limit).to_dict(orient="records")
    keys = list(columns) if columns else (list(rows[0].keys()) if rows else [])
    return [{str(k): json_safe(row.get(k)) for k in keys} for row in rows]


def frame_columns(frame) -> list[str]:
    if hasattr(frame, "columns"):
        return [str(c) for c in frame.columns]
    return []
