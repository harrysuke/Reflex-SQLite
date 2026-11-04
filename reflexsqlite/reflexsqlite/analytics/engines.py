"""Library-specific analysis engines.

Every heavy library is imported lazily inside the function that needs it. A
missing or broken optional dependency becomes a friendly LibraryUnavailableError
instead of crashing the whole app at startup.
"""
from __future__ import annotations

import math
import os
import time
from typing import Any

from ..config import settings
from ..errors import LibraryUnavailableError, ValidationError
from . import plot_utils, registry

Result = dict[str, Any]


# --------------------------------------------------------------------------- #
# Shared helpers
# --------------------------------------------------------------------------- #


def _blank(library_id: str, operation_id: str) -> Result:
    spec = registry.get(library_id)
    op = next((o for o in spec.operations if o.id == operation_id), spec.operations[0])
    return {
        "library": spec.id,
        "library_name": spec.name,
        "library_color": spec.color,
        "operation": op.id,
        "title": op.label,
        "summary": "",
        "metrics": [],
        "table": {"columns": [], "rows": []},
        "chart": [],
        "chart_label": "Value",
        "secondary": False,
        "secondary_label": "",
        "image": "",
        "notes": [],
        "elapsed_ms": 0,
    }


def _fmt(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return "—"
        if abs(value) >= 1000 or (abs(value) < 0.001 and value != 0):
            return f"{value:,.4g}"
        return f"{value:,.3f}".rstrip("0").rstrip(".")
    if isinstance(value, bool):
        return "Yes" if value else "No"
    return str(value)[:48]


def _frame(rows: list[dict[str, Any]], columns: list[str]):
    import pandas as pd

    frame = pd.DataFrame(rows)
    for column in columns:
        if column not in frame.columns:
            frame[column] = None
    return frame[columns]


def _numbers(frame, columns: list[str]):
    import numpy as np
    import pandas as pd

    if not columns:
        return np.zeros((len(frame), 0), dtype=float)
    numeric = frame[columns].apply(pd.to_numeric, errors="coerce").to_numpy(dtype=float)
    # Column-wise mean imputation keeps every estimator well-defined.
    means = np.nanmean(np.where(np.isfinite(numeric), numeric, np.nan), axis=0)
    means = np.nan_to_num(means, nan=0.0)
    indices = np.where(~np.isfinite(numeric))
    numeric[indices] = np.take(means, indices[1])
    return numeric


def _table(result: Result, columns: list[str], rows: list[list[Any]]) -> None:
    result["table"] = {
        "columns": columns,
        "rows": [
            {str(col): _fmt(value) for col, value in zip(columns, row)}
            for row in rows
        ],
    }


def _frame_table(result: Result, frame, max_rows: int = 14) -> None:
    columns = [str(c) for c in frame.columns]
    body = [[row[c] for c in frame.columns] for _, row in frame.head(max_rows).iterrows()]
    _table(result, columns, body)


def _metric(result: Result, label: str, value: Any, hint: str = "") -> None:
    result["metrics"].append({"label": label, "value": _fmt(value), "hint": hint})


def _pick(params: dict[str, Any], key: str, options: list[str], default_index: int = 0) -> str:
    choice = str(params.get(key, "") or "")
    return choice if choice in options else (options[default_index] if options else "")


def _require_numeric(numeric: list[str], minimum: int = 1) -> None:
    if len(numeric) < minimum:
        raise ValidationError(
            f"This operation needs at least {minimum} numeric column(s) in the dataset."
        )


# --------------------------------------------------------------------------- #
# NumPy
# --------------------------------------------------------------------------- #


def _numpy(op: str, frame, meta: dict, params: dict, result: Result) -> None:
    import numpy as np

    numeric = meta["numeric"]
    _require_numeric(numeric)
    matrix = _numbers(frame, numeric)

    if op == "summary":
        rows = []
        for index, column in enumerate(numeric):
            values = matrix[:, index]
            rows.append([
                column, values.size, np.mean(values), np.std(values),
                np.min(values), np.percentile(values, 25), np.median(values),
                np.percentile(values, 75), np.max(values),
            ])
        _table(result, ["Column", "N", "Mean", "Std", "Min", "Q1", "Median", "Q3", "Max"], rows)
        result["chart"] = [
            {"name": c[:18], "value": round(float(np.mean(matrix[:, i])), 3)}
            for i, c in enumerate(numeric[:12])
        ]
        result["chart_label"] = "Mean"
        result["summary"] = f"Vectorized statistics for {len(numeric)} numeric columns over {matrix.shape[0]} rows."
        _metric(result, "Rows", matrix.shape[0])
        _metric(result, "Numeric columns", len(numeric))
        _metric(result, "Total values", matrix.size)

    elif op == "correlation":
        labels = numeric[:8]
        corr = np.corrcoef(_numbers(frame, labels).T) if len(labels) > 1 else np.array([[1.0]])
        _table(result, [""] + labels, [[labels[i]] + list(corr[i]) for i in range(len(labels))])
        base = _pick(params, "y_column", labels)
        base_index = labels.index(base)
        result["chart"] = [
            {"name": labels[i][:18], "value": round(float(corr[base_index, i]), 3)}
            for i in range(len(labels)) if i != base_index
        ]
        result["chart_label"] = f"Corr vs {base}"
        result["summary"] = f"Pearson correlation computed with np.corrcoef against {base}."

    elif op == "normalize":
        means = matrix.mean(axis=0)
        stds = np.where(matrix.std(axis=0) == 0, 1.0, matrix.std(axis=0))
        z = (matrix - means) / stds
        preview = min(10, z.shape[0])
        _table(
            result,
            ["Row"] + numeric[:8],
            [[i + 1] + list(z[i, :8]) for i in range(preview)],
        )
        result["chart"] = [
            {"name": numeric[i][:18], "value": round(float(np.mean(np.abs(z[:, i]))), 3)}
            for i in range(min(12, len(numeric)))
        ]
        result["chart_label"] = "Mean |z|"
        result["summary"] = "Z-score standardization: each column now has mean 0 and std 1."
        result["notes"].append("Preview shows the first 10 normalized rows.")

    else:  # trend
        column = _pick(params, "y_column", numeric)
        series = _numbers(frame, [column])[:, 0]
        window = max(3, min(15, len(series) // 8))
        kernel = np.ones(window) / window
        smoothed = np.convolve(series, kernel, mode="valid")
        step = max(1, len(smoothed) // 24)
        result["chart"] = [
            {
                "name": str(i + 1),
                "value": round(float(smoothed[i]), 3),
                "extra": round(float(series[i + window - 1]), 3),
            }
            for i in range(0, len(smoothed), step)
        ][:24]
        result["chart_label"] = "Moving average"
        result["secondary"] = True
        result["secondary_label"] = column[:18]
        result["summary"] = f"Moving average (window={window}) of {column} via np.convolve."
        _metric(result, "Raw mean", float(series.mean()))
        _metric(result, "Raw std", float(series.std()))
        _metric(result, "Window", window)
    result["notes"].append("Computed entirely with NumPy vectorized operations (no Python loops).")


# --------------------------------------------------------------------------- #
# Pandas
# --------------------------------------------------------------------------- #


def _pandas(op: str, frame, meta: dict, params: dict, result: Result) -> None:
    import pandas as pd

    columns, numeric, categorical = meta["columns"], meta["numeric"], meta["categorical"]

    if op == "head":
        chosen = [c for c in (params.get("x_column"), params.get("y_column")) if c in columns]
        view = frame[chosen] if chosen else frame
        _frame_table(result, view.head(settings.max_preview_rows))
        result["summary"] = f"pandas.DataFrame.head({settings.max_preview_rows}) — {frame.shape[0]} rows × {frame.shape[1]} columns."
        _metric(result, "Shape", f"{frame.shape[0]} × {frame.shape[1]}")
        _metric(result, "Memory (KB)", round(float(frame.memory_usage(deep=True).sum() / 1024), 1))
        result["notes"].append("Use the X / Y selectors to focus on two columns.")

    elif op == "describe":
        if numeric:
            described = frame[numeric].apply(pd.to_numeric, errors="coerce").describe().T.reset_index()
        else:
            described = frame.describe(include="all").T.reset_index()
        _frame_table(result, described, 16)
        result["summary"] = "Descriptive statistics from pandas.DataFrame.describe()."
        result["chart"] = [
            {"name": str(r["index"])[:18], "value": round(float(r["mean"]), 3)}
            for _, r in described.iterrows() if "mean" in described.columns
        ]
        result["chart_label"] = "Mean"

    elif op == "groupby":
        _require_numeric(numeric)
        group = _pick(params, "x_column", categorical or columns)
        value = _pick(params, "y_column", numeric)
        grouped = (
            frame.assign(**{value: pd.to_numeric(frame[value], errors="coerce")})
            .groupby(group, dropna=False)[value]
            .agg(["count", "mean", "sum", "max"])
            .reset_index()
            .sort_values("mean", ascending=False)
            .head(12)
        )
        _frame_table(result, grouped, 12)
        result["chart"] = [
            {"name": str(r[group])[:18], "value": round(float(r["mean"]), 3)}
            for _, r in grouped.iterrows()
        ]
        result["chart_label"] = f"Mean {value}"
        result["summary"] = f"Mean of {value} grouped by {group}, via pandas.groupby()."
        _metric(result, "Groups", len(grouped))

    elif op == "missing":
        counts = frame.isna().sum()
        empties = (frame.astype(str) == "").sum()
        combined = (counts + empties).to_dict()
        _table(result, ["Column", "Missing", "Completeness %"], [
            [c, int(v), round(100 * (1 - int(v) / max(1, len(frame))), 1)] for c, v in combined.items()
        ])
        result["chart"] = [
            {"name": str(c)[:18], "value": int(v)} for c, v in list(combined.items())[:12]
        ]
        result["chart_label"] = "Missing cells"
        result["summary"] = "Null / empty cell audit across every column."
        _metric(result, "Total missing", int(sum(combined.values())))

    else:  # value_counts
        column = _pick(params, "x_column", categorical or columns)
        counts = frame[column].astype(str).value_counts().head(12)
        _table(result, [column, "Count", "Share %"], [
            [key, int(value), round(100 * int(value) / max(1, len(frame)), 1)]
            for key, value in counts.items()
        ])
        result["chart"] = [{"name": str(k)[:18], "value": int(v)} for k, v in counts.items()]
        result["chart_label"] = "Count"
        result["summary"] = f"Top {len(counts)} distinct values of {column} via value_counts()."
    result["notes"].append("Aggregations run on a pandas DataFrame built from the SQLite rows.")


# --------------------------------------------------------------------------- #
# Matplotlib / Seaborn
# --------------------------------------------------------------------------- #


def _matplotlib(op: str, frame, meta: dict, params: dict, result: Result) -> None:
    import numpy as np

    numeric = meta["numeric"]
    _require_numeric(numeric)
    y = _pick(params, "y_column", numeric)
    x = _pick(params, "x_column", numeric, 1 % max(1, len(numeric)))
    series = np.asarray(_numbers(frame, [y])[:, 0], dtype=float)

    if op == "histogram":
        figure, axes = plot_utils.new_figure()
        axes.hist(series, bins=28, color=plot_utils.PALETTE[0], edgecolor="white", linewidth=0.6, alpha=0.9)
        axes.set_title(f"Distribution of {y}")
        axes.set_xlabel(y)
        axes.set_ylabel("Frequency")
    elif op == "line":
        figure, axes = plot_utils.new_figure(8.4, 3.4)
        sample = series[:240]
        axes.plot(range(len(sample)), sample, color=plot_utils.PALETTE[0], linewidth=1.8)
        axes.fill_between(range(len(sample)), sample, alpha=0.10, color=plot_utils.PALETTE[0])
        axes.set_title(f"{y} over source order")
        axes.set_xlabel("Row index")
        axes.set_ylabel(y)
    elif op == "scatter":
        figure, axes = plot_utils.new_figure(6.6, 4.2)
        other = _numbers(frame, [x])[:, 0]
        axes.scatter(other[:400], series[:400], s=22, alpha=0.62, color=plot_utils.PALETTE[1], edgecolor="white", linewidth=0.4)
        axes.set_title(f"{x} vs {y}")
        axes.set_xlabel(x)
        axes.set_ylabel(y)
    else:
        figure, axes = plot_utils.new_figure()
        labels = numeric[:6]
        box_data = [_numbers(frame, [c])[:, 0] for c in labels]
        box_kwargs = dict(
            patch_artist=True,
            boxprops={"facecolor": plot_utils.PALETTE[0], "alpha": 0.65},
            medianprops={"color": "#0F172A"},
            flierprops={"marker": "o", "markersize": 3, "alpha": 0.5},
        )
        # `labels` was renamed to `tick_labels` in Matplotlib 3.9 and removed
        # in 3.11; support both so any 3.x install works.
        try:
            axes.boxplot(box_data, tick_labels=labels, **box_kwargs)
        except TypeError:
            axes.boxplot(box_data, labels=labels, **box_kwargs)
        axes.set_title("Numeric column spread")
        axes.tick_params(axis="x", labelrotation=18)
    result["image"] = plot_utils.figure_to_uri(figure)
    result["summary"] = f"Rendered a Matplotlib figure of {y} ({len(series):,} points)."
    _metric(result, "Points", len(series))
    _metric(result, "Mean", float(series.mean()))
    _metric(result, "Std", float(series.std()))
    _metric(result, "Min / Max", f"{series.min():.2f} / {series.max():.2f}")
    _table(result, ["Statistic", "Value"], [
        ["count", len(series)], ["mean", series.mean()], ["std", series.std()],
        ["p25", np.percentile(series, 25)], ["median", np.median(series)],
        ["p75", np.percentile(series, 75)], ["min", series.min()], ["max", series.max()],
    ])
    result["notes"].append("Figure is rendered server-side with the Agg backend and inlined as a PNG data URI.")


def _seaborn(op: str, frame, meta: dict, params: dict, result: Result) -> None:
    import numpy as np
    import pandas as pd
    import seaborn as sns

    numeric = meta["numeric"]
    _require_numeric(numeric, 2 if op in {"heatmap", "pairwise"} else 1)
    frame_num = frame[numeric[:8]].apply(pd.to_numeric, errors="coerce")
    y = _pick(params, "y_column", numeric)
    categorical = meta["categorical"]

    sns.set_theme(style="whitegrid", palette="deep")
    if op == "heatmap":
        corr = frame_num.corr().fillna(0)
        figure, axes = plot_utils.new_figure(7.2, 5.0)
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0,
                    linewidths=0.5, ax=axes, cbar_kws={"shrink": 0.8},
                    annot_kws={"size": 8})
        axes.set_title("Correlation heatmap")
        axes.tick_params(axis="x", labelrotation=35)
        axes.tick_params(axis="y", labelrotation=0)
    elif op == "distribution":
        figure, axes = plot_utils.new_figure()
        sns.histplot(frame_num[y].dropna(), kde=True, color=plot_utils.PALETTE[0], ax=axes, bins=28)
        axes.set_title(f"Distribution + KDE — {y}")
    elif op == "violin":
        if not categorical:
            raise ValidationError("A categorical column is required for a violin plot.")
        group = _pick(params, "x_column", categorical)
        plot_frame = frame[[group, y]].copy()
        plot_frame[y] = pd.to_numeric(plot_frame[y], errors="coerce")
        top = plot_frame[group].astype(str).value_counts().head(6).index
        plot_frame = plot_frame[plot_frame[group].astype(str).isin(top)]
        figure, axes = plot_utils.new_figure(7.6, 4.0)
        sns.violinplot(data=plot_frame, x=group, y=y, ax=axes, inner="quartile", cut=0)
        axes.set_title(f"{y} by {group}")
        axes.tick_params(axis="x", labelrotation=18)
    else:
        labels = numeric[:4]
        pair = frame_num[labels].dropna().head(220)
        grid = sns.pairplot(pair, diag_kind="kde", plot_kws={"s": 16, "alpha": 0.65})
        grid.figure.set_size_inches(7.6, 6.4)
        figure = grid.figure
    result["image"] = plot_utils.figure_to_uri(figure)
    result["summary"] = f"Seaborn statistical graphic over {len(frame_num.columns)} numeric columns."
    _metric(result, "Rows", len(frame_num))
    _metric(result, "Numeric columns", len(frame_num.columns))
    result["notes"].append("Seaborn uses Matplotlib under the hood; the finished figure is inlined as PNG.")


# --------------------------------------------------------------------------- #
# scikit-learn
# --------------------------------------------------------------------------- #


def _sklearn(op: str, frame, meta: dict, params: dict, result: Result) -> None:
    import numpy as np
    from sklearn.cluster import KMeans
    from sklearn.decomposition import PCA
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import r2_score, silhouette_score
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler

    numeric = meta["numeric"]
    _require_numeric(numeric, 2 if op in {"pca", "forest"} else 1)
    matrix = _numbers(frame, numeric[:10])
    matrix = matrix[: settings.max_training_rows]
    target_name = _pick(params, "y_column", numeric)
    target_index = numeric.index(target_name)
    y = matrix[:, target_index]
    features = [c for i, c in enumerate(numeric[:10]) if i != target_index]
    x = matrix[:, [numeric.index(c) for c in features]] if features else np.ones((len(matrix), 1))
    scaled = StandardScaler().fit_transform(x)

    if op == "kmeans":
        k = min(3, max(2, len(matrix) // 8))
        model = KMeans(n_clusters=k, n_init=8, random_state=0)
        labels = model.fit_predict(scaled)
        score = silhouette_score(scaled, labels) if k > 1 else 0.0
        sizes = np.bincount(labels, minlength=k)
        result["chart"] = [{"name": f"Cluster {i + 1}", "value": int(v)} for i, v in enumerate(sizes)]
        result["chart_label"] = "Rows"
        _table(result, ["Cluster", "Rows", "Centroid norm"], [
            [i + 1, int(sizes[i]), float(np.linalg.norm(model.cluster_centers_[i]))]
            for i in range(k)
        ])
        _metric(result, "Clusters", k)
        _metric(result, "Silhouette", score)
        _metric(result, "Inertia", model.inertia_)
        result["summary"] = f"KMeans (k={k}) on {scaled.shape[1]} standardized features."

    elif op == "linear":
        x_train, x_test, y_train, y_test = train_test_split(scaled, y, test_size=0.25, random_state=0)
        model = LinearRegression().fit(x_train, y_train)
        predictions = model.predict(x_test)
        score = r2_score(y_test, predictions)
        _table(result, ["Feature", "Coefficient"], [
            [features[i] if i < len(features) else "bias", float(coef)]
            for i, coef in enumerate(model.coef_[:12])
        ] + [["intercept", float(model.intercept_)]])
        sample = min(20, len(y_test))
        result["chart"] = [
            {"name": str(i + 1), "value": round(float(y_test[i]), 3), "extra": round(float(predictions[i]), 3)}
            for i in range(sample)
        ]
        result["chart_label"] = "Actual"
        result["secondary"] = True
        result["secondary_label"] = "Predicted"
        _metric(result, "R² (holdout)", score)
        _metric(result, "Train / test", f"{len(y_train)} / {len(y_test)}")
        result["summary"] = f"LinearRegression predicting {target_name} from {len(features)} features."

    elif op == "forest":
        model = RandomForestRegressor(n_estimators=40, max_depth=6, random_state=0, n_jobs=-1)
        model.fit(scaled, y)
        order = np.argsort(model.feature_importances_)[::-1][:10]
        result["chart"] = [
            {"name": (features[i] if i < len(features) else f"f{i}")[:18], "value": round(float(model.feature_importances_[i]), 4)}
            for i in order
        ]
        result["chart_label"] = "Importance"
        _table(result, ["Feature", "Importance"], [
            [features[i] if i < len(features) else f"f{i}", float(model.feature_importances_[i])] for i in order
        ])
        _metric(result, "Trees", 40)
        _metric(result, "Train R²", model.score(scaled, y))
        result["summary"] = f"RandomForestRegressor importance ranking for {target_name}."

    elif op == "pca":
        components = min(3, scaled.shape[1])
        pca = PCA(n_components=components)
        projected = pca.fit_transform(scaled)
        result["chart"] = [
            {"name": f"PC{i + 1}", "value": round(float(pca.explained_variance_ratio_[i]) * 100, 2)}
            for i in range(components)
        ]
        result["chart_label"] = "Variance %"
        _table(result, ["Row", "PC1", "PC2"] + (["PC3"] if components > 2 else []), [
            [i + 1] + list(projected[i, :components]) for i in range(min(10, len(projected)))
        ])
        _metric(result, "Explained variance", float(sum(pca.explained_variance_ratio_)) * 100, "%")
        _metric(result, "Components", components)
        result["summary"] = "PCA projection of standardized numeric features."

    else:  # scale
        _table(result, ["Feature", "Raw mean", "Raw std", "Scaled mean", "Scaled std"], [
            [features[i] if i < len(features) else f"f{i}",
             float(x[:, i].mean()), float(x[:, i].std()),
             float(scaled[:, i].mean()), float(scaled[:, i].std())]
            for i in range(min(10, x.shape[1]))
        ])
        result["chart"] = [{"name": "Before", "value": round(float(np.mean(x.std(axis=0))), 3)},
                           {"name": "After", "value": round(float(np.mean(scaled.std(axis=0))), 3)}]
        result["chart_label"] = "Mean column std"
        result["summary"] = "StandardScaler centers each feature to mean 0 and unit variance."
    result["notes"].append(f"Training capped at {settings.max_training_rows} rows for responsiveness.")


# --------------------------------------------------------------------------- #
# PyTorch
# --------------------------------------------------------------------------- #


def _torch(op: str, frame, meta: dict, params: dict, result: Result) -> None:
    import numpy as np
    import torch

    numeric = meta["numeric"]
    _require_numeric(numeric)
    matrix = _numbers(frame, numeric[:10])[: settings.max_training_rows]
    target_name = _pick(params, "y_column", numeric)
    target_index = numeric.index(target_name)
    y_raw = matrix[:, target_index]
    features = [i for i in range(matrix.shape[1]) if i != target_index]
    x_raw = matrix[:, features] if features else np.ones((len(matrix), 1))
    x_raw = (x_raw - x_raw.mean(axis=0)) / np.where(x_raw.std(axis=0) == 0, 1, x_raw.std(axis=0))
    y_mean, y_std = float(y_raw.mean()), float(y_raw.std() or 1.0)
    x_tensor = torch.tensor(x_raw, dtype=torch.float32)
    y_tensor = torch.tensor((y_raw - y_mean) / y_std, dtype=torch.float32).reshape(-1, 1)

    if op == "tensor_stats":
        _table(result, ["Statistic", "Value"], [
            ["shape", " × ".join(str(v) for v in x_tensor.shape)],
            ["dtype", str(x_tensor.dtype)], ["mean", x_tensor.mean().item()],
            ["std", x_tensor.std().item()], ["min", x_tensor.min().item()],
            ["max", x_tensor.max().item()], ["Frobenius norm", torch.linalg.norm(x_tensor).item()],
            ["device", str(x_tensor.device)],
        ])
        _metric(result, "Tensors", 2)
        _metric(result, "Elements", x_tensor.numel())
        _metric(result, "Autograd ready", "Yes")
        result["chart"] = [
            {"name": (numeric[i] if i < len(numeric) else f"f{i}")[:18], "value": round(float(x_raw[:, i].std()), 3)}
            for i in range(min(10, x_raw.shape[1]))
        ]
        result["chart_label"] = "Std"
        result["summary"] = "Dataset converted to a float32 torch.Tensor and summarized."
        result["notes"].append("Tensors use autograd; switch device to CUDA when a GPU is available.")
        return

    hidden = 16
    if op == "mlp":
        model = torch.nn.Sequential(
            torch.nn.Linear(x_tensor.shape[1], hidden), torch.nn.ReLU(),
            torch.nn.Linear(hidden, hidden // 2), torch.nn.ReLU(),
            torch.nn.Linear(hidden // 2, 1),
        )
        optimizer = torch.optim.Adam(model.parameters(), lr=0.03)
        epochs = 60
    else:
        model = torch.nn.Linear(x_tensor.shape[1], 1)
        optimizer = torch.optim.SGD(model.parameters(), lr=0.06)
        epochs = 45
    loss_fn = torch.nn.MSELoss()
    history: list[float] = []
    for epoch in range(epochs):
        optimizer.zero_grad()
        loss = loss_fn(model(x_tensor), y_tensor)
        loss.backward()
        optimizer.step()
        if epoch % 3 == 0 or epoch == epochs - 1:
            history.append(float(loss.item()))

    with torch.no_grad():
        predictions = (model(x_tensor).numpy().ravel() * y_std) + y_mean
    ss_res = float(np.sum((y_raw - predictions) ** 2))
    ss_tot = float(np.sum((y_raw - y_raw.mean()) ** 2)) or 1.0
    r2 = 1 - ss_res / ss_tot

    result["chart"] = [
        {"name": f"E{i * 3 + 1}", "value": round(v, 5)} for i, v in enumerate(history)
    ]
    result["chart_label"] = "MSE loss"
    _table(result, ["Epoch", "Loss"], [[i * 3 + 1, v] for i, v in enumerate(history[-10:])])
    _metric(result, "Epochs", epochs)
    _metric(result, "Final loss", history[-1])
    _metric(result, "R² (train)", r2)
    _metric(result, "Parameters", sum(p.numel() for p in model.parameters()))
    result["summary"] = f"Trained a {'2-hidden-layer MLP' if op == 'mlp' else 'linear layer'} with autograd + {'Adam' if op == 'mlp' else 'SGD'} to predict {target_name}."
    result["notes"].append("Loss is MSE on standardized targets; the chart shows the training curve.")


# --------------------------------------------------------------------------- #
# TensorFlow / Keras
# --------------------------------------------------------------------------- #


def _tensorflow(op: str, frame, meta: dict, params: dict, result: Result) -> None:
    os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
    os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS", "0")
    import numpy as np
    import tensorflow as tf

    numeric = meta["numeric"]
    _require_numeric(numeric)
    matrix = _numbers(frame, numeric[:10])[: settings.max_training_rows]
    constant = tf.constant(matrix, dtype=tf.float32)

    if op == "tensor_stats":
        values = [
            ["shape", " × ".join(str(int(v)) for v in constant.shape)],
            ["dtype", constant.dtype.name],
            ["mean", float(tf.reduce_mean(constant))],
            ["std", float(tf.math.reduce_std(constant))],
            ["min", float(tf.reduce_min(constant))],
            ["max", float(tf.reduce_max(constant))],
            ["sum", float(tf.reduce_sum(constant))],
        ]
        _table(result, ["Statistic", "Value"], values)
        _metric(result, "Elements", int(tf.size(constant)))
        _metric(result, "Rank", int(tf.rank(constant)))
        _metric(result, "Eager execution", str(tf.executing_eagerly()))
        result["chart"] = [
            {"name": (numeric[i] if i < len(numeric) else f"f{i}")[:18],
             "value": round(float(tf.reduce_mean(constant[:, i])), 3)}
            for i in range(min(10, matrix.shape[1]))
        ]
        result["chart_label"] = "Mean"
        result["summary"] = "Dataset wrapped in a tf.Tensor and reduced with TensorFlow ops."
        result["notes"].append("tf.reduce_* ops run eagerly on CPU.")
        return

    target_name = _pick(params, "y_column", numeric)
    target_index = numeric.index(target_name)
    y_raw = matrix[:, target_index]
    feature_indices = [i for i in range(matrix.shape[1]) if i != target_index]
    x_raw = matrix[:, feature_indices] if feature_indices else np.ones((len(matrix), 1))
    x_raw = (x_raw - x_raw.mean(axis=0)) / np.where(x_raw.std(axis=0) == 0, 1, x_raw.std(axis=0))

    if op == "keras_classifier":
        candidates = [c for c in meta["categorical"] if 1 < frame[c].nunique() <= 6]
        if not candidates:
            raise ValidationError("A categorical column with 2-6 distinct values is required.")
        target = _pick(params, "x_column", candidates)
        classes = sorted(frame[target].astype(str).unique())[: len(matrix)]
        lookup = {name: i for i, name in enumerate(classes)}
        labels = np.array([lookup.get(str(v), 0) for v in frame[target].astype(str)[: len(matrix)]])
        y_train = tf.keras.utils.to_categorical(labels, num_classes=len(classes))
        model = tf.keras.Sequential([
            tf.keras.Input(shape=(x_raw.shape[1],)),
            tf.keras.layers.Dense(24, activation="relu"),
            tf.keras.layers.Dense(12, activation="relu"),
            tf.keras.layers.Dense(len(classes), activation="softmax"),
        ])
        model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
        epochs = 14
        chart_key, chart_label = "accuracy", "Accuracy"
        monitor = "accuracy"
    else:
        y_mean, y_std = float(y_raw.mean()), float(y_raw.std() or 1.0)
        y_train = (y_raw - y_mean) / y_std
        model = tf.keras.Sequential([
            tf.keras.Input(shape=(x_raw.shape[1],)),
            tf.keras.layers.Dense(16, activation="relu"),
            tf.keras.layers.Dense(8, activation="relu"),
            tf.keras.layers.Dense(1),
        ])
        model.compile(optimizer=tf.keras.optimizers.Adam(0.02), loss="mse", metrics=["mae"])
        epochs = 14
        chart_key, chart_label = "loss", "MSE loss"
        monitor = "loss"

    history = model.fit(x_raw, y_train, epochs=epochs, batch_size=24, verbose=0)
    curve = [float(v) for v in history.history[chart_key]]
    result["chart"] = [{"name": f"E{i + 1}", "value": round(v, 5)} for i, v in enumerate(curve)]
    result["chart_label"] = chart_label
    _table(result, ["Epoch", chart_label], [[i + 1, v] for i, v in enumerate(curve)])
    _metric(result, "Epochs", epochs)
    _metric(result, "Parameters", int(model.count_params()))
    _metric(result, f"Final {chart_label}", curve[-1])
    _metric(result, "Backend", "TensorFlow / Keras")
    result["summary"] = f"Keras dense network trained for {epochs} epochs on {len(x_raw)} rows."
    result["notes"].append(f"Monitored metric: {monitor}. Training is capped at {settings.max_training_rows} rows.")


# --------------------------------------------------------------------------- #
# Public entry point
# --------------------------------------------------------------------------- #

_DISPATCH = {
    "numpy": _numpy,
    "pandas": _pandas,
    "matplotlib": _matplotlib,
    "seaborn": _seaborn,
    "sklearn": _sklearn,
    "torch": _torch,
    "tensorflow": _tensorflow,
}


def run(
    library_id: str,
    operation_id: str,
    meta: dict[str, Any],
    rows: list[dict[str, Any]],
    params: dict[str, Any] | None = None,
) -> Result:
    """Execute one library operation against dataset rows and return UI-ready data."""
    started = time.perf_counter()
    spec = registry.require(library_id)
    params = params or {}
    result = _blank(library_id, operation_id)
    if not rows:
        raise ValidationError("Select a dataset with at least one row first.")
    try:
        frame = _frame(rows, meta["columns"])
        _DISPATCH[spec.id](operation_id, frame, meta, params, result)
    except ImportError as exc:
        raise LibraryUnavailableError(
            f"{spec.name} could not be imported ({exc}). Run `{spec.install}`."
        ) from exc
    except (LibraryUnavailableError, ValidationError):
        raise
    result["elapsed_ms"] = int((time.perf_counter() - started) * 1000)
    result["notes"].append(f"Executed with {spec.name} in {result['elapsed_ms']} ms.")
    return result
