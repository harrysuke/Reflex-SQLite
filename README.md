# Reflex-SQLite Application

A full-stack data-science workspace built with **Reflex** (pure-Python UI + reactive
state) and an **SQLite** database, extended with a standalone **`ml_pipelines/`**
package for statistical modelling, predictive analytics and large-scale mining.

## Features

* **Pure Python full-stack** — Reflex renders the frontend and runs the reactive
  state handlers; no JavaScript is written by hand.
* **SQLite persistence** — arbitrary datasets are stored row-by-row as JSON in
  `dataset_rows`, queried with raw parameterized SQL (`json_extract`).
* **Statistical profiling** — uploading a CSV/Excel file triggers a background
  scipy suite: descriptive statistics, Shapiro-Wilk normality, Pearson correlation
  matrices with p-values, and t-tests / one-way ANOVA across categorical groups.
* **Regression & forecasting** — statsmodels OLS (coefficients, p-values,
  confidence intervals) and ARIMA/SARIMAX forecasts with confidence bands and
  additive trend/seasonality decomposition, rendered with `rx.recharts`.
* **Predictive analytics** — an offline trainer fits a scikit-learn pipeline
  (Random Forest / Gradient Boosting / XGBoost / LightGBM / linear), saves it to
  `models/*.joblib`, and the backend loads it **once at startup**. Every CRUD
  create/update runs `model.predict()` and logs the call to `model_logs`.
* **Drift monitoring** — rolling accuracy / MAE over resolved predictions, with
  an outcome-recording workflow to close the feedback loop.
* **DuckDB OLAP** — `ATTACH` the live SQLite file and run vectorized, columnar
  SQL over the `rows_flat` view without copying or migrating data.
* **Out-of-core files** — `polars.scan_csv()` + streaming aggregation for files
  larger than RAM.
* **Unsupervised mining** — K-Means / HDBSCAN segmentation and mlxtend
  FP-Growth / Apriori association rules.

## Project Structure

```text
├── data/                  # SQLite database (app.db)
├── uploads/               # Raw uploads + large-file mining source
├── models/                # Trained .joblib artifacts + active.json
├── ml_pipelines/          # Standalone ML/data pipelines (no Reflex imports)
│   ├── data_access.py     #   SQLite -> pandas / polars bridge (raw SQL)
│   ├── preprocessing.py   #   Shared feature engineering + estimator factory
│   ├── statistics.py      #   scipy profiling suite
│   ├── regression.py      #   statsmodels OLS + ARIMA/SARIMAX
│   ├── train.py           #   Offline training -> models/*.joblib
│   ├── inference.py       #   Single-load, mtime-aware model registry
│   ├── drift.py           #   Rolling accuracy / MAE from model_logs
│   ├── olap.py            #   DuckDB SQLite scanner + rows_flat view
│   ├── large_files.py     #   Polars lazy scan + streaming aggregation
│   ├── mining.py          #   Clustering + association rules
│   ├── paths.py           #   Runtime path resolution (CLI + backend)
│   └── __main__.py        #   `python -m ml_pipelines ...` CLI
├── reflexsqlite/          # Reflex application
│   ├── reflexsqlite/
│   │   ├── models.py      #   SQLModel tables (incl. model_logs, ml_models)
│   │   ├── repositories.py#   The only module that issues queries
│   │   ├── services/      #   dataset_service, auth_service, ml_service
│   │   ├── state/         #   AuthState + page states (background events)
│   │   ├── components/    #   layout, charts, ui primitives, theme
│   │   └── pages/         #   dashboard, datasets, explore, statistics,
│   │                      #   models, mining, settings, auth
│   └── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

* Python 3.10 or higher
* pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/harrysuke/Reflex-SQLite.git
   cd Reflex-SQLite
   ```
2. Install the application and analytics dependencies:
   ```bash
   cd reflexsqlite
   pip install -r requirements.txt
   ```
   Or let the bootstrap script create a project `.venv` and install everything
   into it (recommended — it also verifies that each library imports):
   ```bash
   python scripts/bootstrap.py
   ```
3. Initialize the Reflex project (first run only):
   ```bash
   reflex init
   ```

### Running the Application

```bash
cd reflexsqlite
reflex run
```
Alternatively, with `uv` — note that `uv add reflex` alone is **not** enough, it
installs only the web framework and leaves pandas/scipy missing:

```bash
cd reflexsqlite
uv venv
uv pip install -r requirements.txt
uv run reflex run
```

The app initializes the SQLite schema (including `model_logs` and `ml_models`),
seeds demo data on an empty database, warm-starts the active `.joblib` model, and
serves the UI at `http://localhost:3000`.

### Troubleshooting: "pandas is not available"

This means the Python process running the **backend** cannot import the package.
It is almost always an environment mismatch, not a code problem: `reflex run`
only requires Reflex, so a bare `pip install reflex` / `uv add reflex` boots the
UI and then fails on the first pandas call.

Diagnose it with the interpreter that runs the app:

```bash
python -m ml_pipelines check
```

It prints the exact interpreter path, the real import status of every library,
and the command that fixes it. Two ways to resolve:

* **Install the missing packages into that interpreter**
  ```bash
  "<the interpreter printed above>" -m pip install -r reflexsqlite/requirements.txt
  ```
* **Use the audited environment** created by `python scripts/bootstrap.py`, then
  start the app with `.venv/Scripts/python.exe -m reflex run`.

The same audit is available in the UI under **Settings → Dependency audit**,
which imports each library for real and shows the per-package fix command.

## Pages

| Route | Purpose |
| --- | --- |
| `/dashboard` | KPI cards, interactive charts, correlation grid, live feed |
| `/datasets` | Upload, browse, create/edit/delete rows; auto-profiles uploads |
| `/explore` | Library workbench (numpy / pandas / sklearn / ...) |
| `/statistics` | scipy hypothesis tests, OLS regression, ARIMA forecasting |
| `/models` | Training, model registry, live inference, drift monitoring |
| `/mining` | DuckDB OLAP console, Polars large files, clustering, association rules |

## Offline CLI

The pipelines run without the web app (from the workspace root):

```bash
python -m ml_pipelines check
python -m ml_pipelines profile --dataset-id 1
python -m ml_pipelines train   --dataset-id 1 --target revenue --algorithm xgboost
python -m ml_pipelines predict --input '{"units": 12, "unit_price": 49.9}'
```

## Architecture Notes

* **Separation of concerns** — `ml_pipelines` never imports Reflex; the UI never
  imports pandas / scikit-learn. `services/ml_service.py` is the only bridge.
* **Background events** — training, profiling, OLAP, clustering and association
  rule mining run in `@rx.event(background=True)` handlers, offloaded with
  `asyncio.to_thread`, so the websocket loop never blocks.
* **Resilient dependencies** — optional analytics libraries are imported lazily.
  A missing library raises a friendly `LibraryUnavailableError`; a blocked
  compiled DLL degrades to the next available estimator instead of crashing.
* **Schema parity** — `ml_models` is defined identically in SQLModel and in the
  CLI's `CREATE TABLE IF NOT EXISTS`, so either path can register artifacts.
