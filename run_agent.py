#!/usr/bin/env python3
"""
Run script for PhantomGuard Agent
"""

import os
import subprocess
from pathlib import Path


def run_agent():
    agent_dir = Path(__file__).parent / "agent"
    venv_dir = agent_dir / "venv"
    if not venv_dir.exists():
        print("Agent virtual environment not found. Run setup_dev.bat first.")
        return

    if os.name == "nt":
        python_exe = str(venv_dir / "Scripts" / "python.exe")
    else:
        python_exe = str(venv_dir / "bin" / "python")

    env = os.environ.copy()
    env["PYTHONPATH"] = str(agent_dir)

    subprocess.run([python_exe, "-m", "src.main"], cwd=str(agent_dir), env=env)


if __name__ == "__main__":
    run_agent()
