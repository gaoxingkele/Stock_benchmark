"""Small .env loader used by local scripts.

The project avoids printing secret values. This loader only places values in
the process environment and returns the loaded variable names.
"""

from __future__ import annotations

import os
from pathlib import Path


def load_dotenv(path: str | Path, override: bool = False) -> list[str]:
    """Load KEY=VALUE pairs from a dotenv file.

    Args:
        path: Dotenv file path.
        override: Whether to overwrite variables already present in env.

    Returns:
        Names of variables loaded or already present when override is false.
    """

    env_path = Path(path)
    if not env_path.exists():
        return []

    loaded: list[str] = []
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if not key:
            continue
        if override or key not in os.environ:
            os.environ[key] = value
        loaded.append(key)
    return loaded


def load_project_env(project_root: str | Path) -> list[str]:
    """Load project-level dotenv files in the expected order."""

    root = Path(project_root)
    loaded: list[str] = []
    loaded.extend(load_dotenv(root / ".env"))
    loaded.extend(load_dotenv(root / ".env.cloubic"))
    return loaded

