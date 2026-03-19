#!/usr/bin/env python3
"""
Run script for PhantomGuard Backend
"""

import os
import subprocess
from pathlib import Path


def run_backend():
    backend_dir = Path(__file__).parent / "backend"
    venv_dir = backend_dir / "venv"
    if not venv_dir.exists():
        print("Backend virtual environment not found. Run setup_dev.bat first.")
        return

    if os.name == "nt":
        python_exe = str(venv_dir / "Scripts" / "python.exe")
    else:
        python_exe = str(venv_dir / "bin" / "python")

    uvicorn_cmd = [
        python_exe,
        "-m",
        "uvicorn",
        "app.main:app",
        "--host",
        "0.0.0.0",
        "--port",
        "8000",
    ]

    env = os.environ.copy()
    env["PYTHONPATH"] = str(backend_dir)

    print("Starting PhantomGuard Backend...")
    print("API documentation: http://localhost:8000/docs")
    print("Health check: http://localhost:8000/health")

    try:
        subprocess.run(
            [python_exe, "-c", "from app.database.init_db import create_tables; create_tables()"],
            cwd=str(backend_dir),
            env=env,
            check=True,
        )
        subprocess.run(uvicorn_cmd, cwd=str(backend_dir), env=env)
    except KeyboardInterrupt:
        print("\nBackend stopped")
    except Exception as exc:
        print(f"Failed to start backend: {exc}")


if __name__ == "__main__":
    run_backend()
