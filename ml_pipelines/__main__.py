"""Command-line entry point for the offline ML pipelines.

    python -m ml_pipelines check
    python -m ml_pipelines train --dataset-id 1 --target revenue
    python -m ml_pipelines profile --dataset-id 1
    python -m ml_pipelines predict --input '{"units": 12, "unit_price": 49.9}'
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any


def _print(data: Any) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False, default=str))


def _cmd_check(args: argparse.Namespace) -> int:
    from ._optional import diagnostics
    from .paths import database_path, models_dir, uploads_dir

    report = diagnostics()
    paths = {
        "database": str(database_path()),
        "models": str(models_dir()),
        "uploads": str(uploads_dir()),
    }

    if getattr(args, "json", False):
        _print({"paths": paths, **report})
        return 0 if report["ready"] else 1

    python = report["python"]
    print("DataForge environment check")
    print("-" * 68)
    print(f"interpreter : {python['executable']}")
    print(f"version     : {python['version']}"
          f" ({'virtualenv' if python['virtual_env'] else 'system/base Python'})")
    print(f"database    : {paths['database']}")
    print(f"models      : {paths['models']}")
    print(f"uploads     : {paths['uploads']}")
    print()

    for group in report["groups"]:
        flag = "required" if group["required"] else "optional"
        print(f"[{group['tier']}] ({flag})")
        for row in group["rows"]:
            status = row["status"].upper().ljust(8)
            version_text = row["version"] or "-"
            print(f"  {status} {row['label']:<14} {version_text}")
            if row["status"] != "ok" and row["error"]:
                print(f"           {row['error']}")
        print()

    if report["ready"]:
        print("All required libraries are importable. Everything is ready.")
        return 0

    print("Required libraries are missing or broken:")
    for module in report["missing"]:
        print(f"  - {report['packages'][module]['label']} is not installed")
    for module in report["broken"]:
        print(f"  - {report['packages'][module]['label']} is installed but cannot be imported")
    print()
    print("Fix everything at once, for THIS interpreter:")
    print(f"  {report['fix']}")
    print()
    print("Or install the failing package alone:")
    for module in [*report["missing"], *report["broken"]]:
        print(f"  {report['packages'][module]['fix']}")
    return 1


def _cmd_train(args: argparse.Namespace) -> int:
    from .inference import registry
    from .train import register_model_cli, train_model

    metadata = train_model(
        args.dataset_id,
        args.target,
        algorithm=args.algorithm,
        task=args.task,
        name=args.name,
        max_rows=args.max_rows,
        db_path=args.db_path,
    )
    if not args.no_register:
        register_model_cli(metadata, db_path=args.db_path)
    registry().reload()
    _print({"status": "trained", "model": metadata, "loaded": registry().describe()})
    return 0


def _cmd_profile(args: argparse.Namespace) -> int:
    from .data_access import load_dataset
    from .statistics import profile_frame

    frame = load_dataset(args.dataset_id, db_path=args.db_path)
    report = profile_frame(frame)
    report.pop("charts", None)
    report["correlation_rows"] = f"[{len(report['correlation_rows'])} rows]"
    _print(report)
    return 0


def _cmd_predict(args: argparse.Namespace) -> int:
    from .inference import warm_start

    warm_start()
    from .inference import predict

    features = json.loads(args.input)
    result = predict(features)
    if result is None:
        _print({"status": "no_model", "hint": "Train a model first: python -m ml_pipelines train --help"})
        return 1
    _print({"status": "ok", "prediction": result})
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ml_pipelines", description="DataForge offline ML pipelines")
    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser(
        "check",
        help="Verify that every dependency imports in the current interpreter",
    )
    check.add_argument("--json", action="store_true", help="Machine-readable report")
    check.set_defaults(func=_cmd_check)

    train = sub.add_parser("train", help="Train a model from SQLite and save models/<name>.joblib")
    train.add_argument("--dataset-id", type=int, required=True)
    train.add_argument("--target", required=True)
    train.add_argument("--algorithm", default="random_forest", choices=[
        "random_forest", "gradient_boosting", "linear", "xgboost", "lightgbm"
    ])
    train.add_argument("--task", default=None, choices=["classification", "regression"])
    train.add_argument("--name", default=None)
    train.add_argument("--max-rows", type=int, default=20000)
    train.add_argument("--db-path", default=None)
    train.add_argument("--no-register", action="store_true", help="Do not register the artifact in ml_models")
    train.set_defaults(func=_cmd_train)

    profile = sub.add_parser("profile", help="Run the automated scipy profiling suite")
    profile.add_argument("--dataset-id", type=int, required=True)
    profile.add_argument("--db-path", default=None)
    profile.set_defaults(func=_cmd_profile)

    predict = sub.add_parser("predict", help="Run one inference through the cached .joblib model")
    predict.add_argument("--input", required=True, help="JSON object of input features")
    predict.set_defaults(func=_cmd_predict)

    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except Exception as exc:
        print(json.dumps({"status": "error", "type": type(exc).__name__, "message": str(exc)}, indent=2))
        return 2


if __name__ == "__main__":
    sys.exit(main())
