"""Unsupervised pattern mining: clustering and association rules.

* K-Means / HDBSCAN segment database rows into behavioural groups.
* mlxtend Apriori / FP-Growth discover frequent itemsets and "bought together"
  rules from transactional SQLite tables.
"""
from __future__ import annotations

import warnings
from typing import Any, Sequence

import numpy as np

from ._optional import require
from .preprocessing import clean_frame, json_safe, numeric_columns

MAX_CLUSTER_ROWS = 5000
MAX_BASKETS = 4000
MAX_ITEMS = 40


def _matrix(frame, features: Sequence[str] | None, max_rows: int):
    pd = require("pandas")
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import StandardScaler

    working = clean_frame(frame)
    candidates = numeric_columns(working) if not features else [f for f in features if f in working.columns]
    chosen = [c for c in candidates if working[c].notna().any()][:10]
    if len(chosen) < 2:
        raise ValueError("Clustering needs at least two numeric feature columns.")
    matrix = (
        working[chosen]
        .apply(pd.to_numeric, errors="coerce")
        .replace([np.inf, -np.inf], np.nan)
        .head(max_rows)
    )
    matrix = matrix.dropna(axis=1, how="all")
    chosen = [c for c in chosen if c in matrix.columns]
    matrix = matrix.dropna(how="any")
    if len(matrix) < 6:
        raise ValueError("Not enough complete rows for clustering (need at least 6).")
    values = SimpleImputer(strategy="median").fit_transform(matrix[chosen])
    scaled = StandardScaler().fit_transform(values)
    return matrix, chosen, scaled


def cluster_frame(
    frame,
    *,
    features: Sequence[str] | None = None,
    k: int = 3,
    algorithm: str = "kmeans",
    max_rows: int = MAX_CLUSTER_ROWS,
) -> dict[str, Any]:
    """Segment rows with K-Means or HDBSCAN and return a 2-D PCA scatter."""
    from sklearn.cluster import KMeans
    from sklearn.decomposition import PCA
    from sklearn.metrics import silhouette_score

    matrix, chosen, scaled = _matrix(frame, features, max_rows)
    k = max(2, min(int(k), 8, len(matrix) // 3))
    if algorithm == "hdbscan":
        try:
            from sklearn.cluster import HDBSCAN

            labels = HDBSCAN(min_cluster_size=max(3, len(matrix) // 30)).fit_predict(scaled)
        except ImportError:
            labels = KMeans(n_clusters=k, n_init=10, random_state=42).fit_predict(scaled)
            algorithm = "kmeans"
    else:
        algorithm = "kmeans"
        labels = KMeans(n_clusters=k, n_init=10, random_state=42).fit_predict(scaled)

    projected = PCA(n_components=2, random_state=42).fit_transform(scaled)
    groups = sorted(set(int(v) for v in labels))
    score = None
    if len(groups) > 1 and all(sum(labels == g) > 1 for g in groups):
        try:
            score = float(silhouette_score(scaled, labels))
        except Exception:
            score = None

    columns = ["Cluster", "Rows", "Share %"] + [f"Mean {c[:14]}" for c in chosen[:5]]
    rows: list[dict[str, Any]] = []
    size_chart: list[dict[str, Any]] = []
    for group in groups:
        mask = labels == group
        label = "noise" if group == -1 else f"Cluster {group + 1}"
        record: dict[str, Any] = {
            "Cluster": label,
            "Rows": int(mask.sum()),
            "Share %": round(100 * float(mask.sum()) / len(labels), 1),
        }
        for column in chosen[:5]:
            record[f"Mean {column[:14]}"] = round(float(matrix.loc[mask, column].mean()), 3)
        rows.append(record)
        size_chart.append({"name": label, "value": int(mask.sum())})

    sample = min(360, len(labels))
    step = max(1, len(labels) // sample)
    scatter = [
        {
            "name": f"row{i + 1}",
            "x": round(float(projected[i, 0]), 3),
            "y": round(float(projected[i, 1]), 3),
            "cluster": int(labels[i]),
        }
        for i in range(0, len(labels), step)
    ][:sample]

    metrics = [
        {"label": "Rows", "value": len(matrix), "hint": "Complete numeric rows"},
        {"label": "Features", "value": len(chosen), "hint": ", ".join(chosen[:3])},
        {"label": "Segments", "value": len(groups), "hint": "Including noise when using HDBSCAN"},
        {"label": "Silhouette", "value": round(score, 3) if score is not None else None, "hint": "Higher is better"},
    ]
    return {
        "algorithm": algorithm.upper(),
        "features": chosen,
        "columns": columns,
        "rows": rows,
        "metrics": metrics,
        "chart": size_chart,
        "scatter": scatter,
        "notes": [
            "Features are median-imputed and standardized before clustering.",
            "The scatter is a 2-component PCA projection of the standardized feature space.",
            "HDBSCAN labels -1 as noise; it falls back to K-Means on older scikit-learn builds.",
        ],
    }


def _baskets(frame, transaction_col: str, item_col: str):
    pd = require("pandas")
    from mlxtend.preprocessing import TransactionEncoder

    working = clean_frame(frame)
    if transaction_col not in working.columns or item_col not in working.columns:
        raise ValueError("Transaction and item columns must exist in the dataset.")
    working = working[[transaction_col, item_col]].dropna()
    working[transaction_col] = working[transaction_col].astype(str)
    working[item_col] = working[item_col].astype(str)
    # Keep only the most frequent items so the one-hot matrix stays tractable.
    top_items = (
        working[item_col].value_counts().head(MAX_ITEMS).index.tolist()
    )
    working = working[working[item_col].isin(top_items)]
    transactions = (
        working.groupby(transaction_col)[item_col]
        .apply(lambda values: sorted(set(str(v) for v in values)))
        .tolist()
    )
    transactions = [t for t in transactions if t][:MAX_BASKETS]
    if len(transactions) < 3:
        raise ValueError("Need at least 3 non-empty transactions for association rule mining.")
    encoder = TransactionEncoder()
    # <= 40 items x <= 4000 baskets: a dense bool frame is small and avoids
    # sparse-dtype fill_value warnings in recent pandas releases.
    encoded = encoder.fit(transactions).transform(transactions)
    basket = pd.DataFrame(encoded, columns=[str(c) for c in encoder.columns_], dtype=bool)
    return basket, transactions, top_items


def association_rules(
    frame,
    *,
    transaction_col: str,
    item_col: str,
    algorithm: str = "apriori",
    min_support: float = 0.05,
    metric: str = "lift",
    min_threshold: float = 1.0,
) -> dict[str, Any]:
    """Discover frequent itemsets and rules with mlxtend Apriori or FP-Growth."""
    require("mlxtend")
    from mlxtend.frequent_patterns import association_rules as ml_association_rules
    from mlxtend.frequent_patterns import apriori, fpgrowth

    basket, transactions, top_items = _baskets(frame, transaction_col, item_col)
    finder = fpgrowth if algorithm == "fpgrowth" else apriori
    algorithm = "fpgrowth" if algorithm == "fpgrowth" else "apriori"
    with warnings.catch_warnings():
        # mlxtend divides by zero while computing certainty factor on perfectly
        # deterministic rules; the resulting column is not one we surface.
        warnings.simplefilter("ignore", RuntimeWarning)
        frequent = finder(basket, min_support=float(min_support), use_colnames=True)
        if frequent.empty:
            raise ValueError("No frequent itemsets at this support level. Try lowering minimum support.")
        frequent = frequent.assign(length=frequent["itemsets"].apply(len)).sort_values(
            ["support", "length"], ascending=[False, True]
        )
        rules = ml_association_rules(
            frequent.drop(columns=["length"]),
            metric=metric if metric in {"support", "confidence", "lift", "leverage", "conviction"} else "lift",
            min_threshold=float(min_threshold),
        )
    rules = rules.sort_values(["lift", "confidence"], ascending=False).head(30)

    def names(values) -> str:
        return ", ".join(sorted(str(v) for v in values))

    rule_columns = ["Antecedents", "Consequents", "Support", "Confidence", "Lift", "Leverage", "Conviction"]
    rule_rows: list[dict[str, Any]] = []
    for _, row in rules.iterrows():
        rule_rows.append({
            "Antecedents": names(row["antecedents"]),
            "Consequents": names(row["consequents"]),
            "Support": round(float(row["support"]), 4),
            "Confidence": round(float(row["confidence"]), 4),
            "Lift": round(float(row["lift"]), 3),
            "Leverage": round(float(row.get("leverage", 0.0)), 4),
            "Conviction": json_safe(round(float(row.get("conviction", 0.0)), 3)),
        })

    itemset_columns = ["Itemset", "Size", "Support", "Transactions"]
    itemset_rows = [
        {
            "Itemset": names(row["itemsets"]),
            "Size": int(row["length"]),
            "Support": round(float(row["support"]), 4),
            "Transactions": int(round(float(row["support"]) * len(transactions))),
        }
        for _, row in frequent.head(20).iterrows()
    ]
    chart = [
        {"name": f"{r['Antecedents'][:12]} → {r['Consequents'][:12]}", "value": r["Lift"]}
        for r in rule_rows[:12]
    ]
    metrics = [
        {"label": "Transactions", "value": len(transactions), "hint": "Distinct baskets analysed"},
        {"label": "Distinct items", "value": len(top_items), "hint": "Capped at 40 most frequent"},
        {"label": "Frequent itemsets", "value": int(len(frequent)), "hint": f"min_support={min_support}"},
        {"label": "Rules", "value": len(rule_rows), "hint": f"{metric} ≥ {min_threshold}"},
    ]
    return {
        "algorithm": algorithm.upper(),
        "transaction_col": transaction_col,
        "item_col": item_col,
        "rule_columns": rule_columns,
        "rule_rows": rule_rows,
        "itemset_columns": itemset_columns,
        "itemset_rows": itemset_rows,
        "chart": chart,
        "metrics": metrics,
        "notes": [
            f"mlxtend {algorithm} one-hot encodes transactions (TransactionEncoder, sparse matrix).",
            "Rules are ranked by lift > confidence; lift > 1 means the items occur together more often than expected.",
            "Only the 40 most frequent items are kept to bound the itemset lattice.",
        ],
    }
