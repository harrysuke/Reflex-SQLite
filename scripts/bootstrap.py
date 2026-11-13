"""One-command environment setup for DataForge (Reflex-SQLite).

Why this exists
---------------
``reflex run`` only needs Reflex itself, so an environment created with
``uv add reflex`` / ``pip install reflex`` boots the UI and then fails on the
first pandas call with "pandas is not available". This script creates a project
``.venv`` and installs *every* dependency declared in
``reflexsqlite/requirements.txt`` into it, then verifies that each library
actually imports.

Usage
-----
    python scripts/bootstrap.py            # create .venv + install everything
    python scripts/bootstrap.py --check    # only audit the current interpreter
    python scripts/bootstrap.py --python C:\\path\\to\\python.exe

On Windows the finished environment is started with:

    .venv\\Scripts\\python.exe -m reflex run
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIREMENTS = ROOT / "reflexsqlite" / "requirements.txt"
VENV = ROOT / ".venv"


def venv_python(venv: Path = VENV) -> Path:
    return venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def _run(command: list[str], **kwargs) -> int:
    print(f"\n$ {' '.join(command)}", flush=True)
    return subprocess.call(command, cwd=str(ROOT), **kwargs)


def check(python: str) -> int:
    """Import every dependency in ``python`` and report what is broken."""
    return _run([python, "-m", "ml_pipelines", "check"])


def install(python: str) -> int:
    if not REQUIREMENTS.exists():
        print(f"Missing requirements file: {REQUIREMENTS}")
        return 2
    _run([python, "-m", "pip", "install", "--upgrade", "pip"])
    code = _run([python, "-m", "pip", "install", "-r", str(REQUIREMENTS)])
    if code != 0:
        print("\nInstallation failed. Fix the error above and re-run this script.")
        return code
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Set up the DataForge environment")
    parser.add_argument("--check", action="store_true", help="Only audit an interpreter")
    parser.add_argument("--python", default="", help="Interpreter to install into")
    parser.add_argument("--no-venv", action="store_true", help="Install into --python instead of .venv")
    args = parser.parse_args(argv)

    if args.check:
        return check(args.python or sys.executable)

    if args.python:
        target = args.python
    elif args.no_venv:
        target = sys.executable
    else:
        target = str(venv_python())
        if not Path(target).exists():
            print(f"Creating virtual environment at {VENV}")
            code = _run([sys.executable, "-m", "venv", str(VENV)])
            if code != 0:
                return code

    code = install(target)
    if code != 0:
        return code

    print("\nVerifying imports...")
    check(target)

    quoted = f'"{target}"' if " " in target else target
    print(
        "\nDone. Start the app with:\n"
        f"  cd {ROOT / 'reflexsqlite'}\n"
        f"  {quoted} -m reflex run\n"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
