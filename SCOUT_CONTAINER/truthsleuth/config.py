"""
TruthSleuth configuration.

Re-pointed 2026-08-26 off Android-era hardcoded paths (/storage/emulated/0/...)
to env-overridable Crostini defaults. This module is the lowest-level dependency:
it must never import other truthsleuth modules (per TRUTHSLEUTH.md).

Env overrides:
  TRUTHSLEUTH_ROOT       absolute path to the monitored project root
                         (default: ~/RootBase if it exists)
  TRUTHSLEUTH_PATHS      comma-separated paths RELATIVE to ROOT_DIR to monitor
                         (empty/absent = monitor the whole ROOT_DIR)
  TRUTHSLEUTH_MOLT_ENGINE  absolute path to the Molt engine entry point
"""
import os
from pathlib import Path
from typing import List, Optional


def _resolve_root_dir() -> Path:
    """Resolve the monitored project root (Crostini-first, env-overridable)."""
    env = os.environ.get("TRUTHSLEUTH_ROOT") or os.environ.get("ROOTBASE_DIR")
    if env:
        return Path(env).expanduser().resolve()

    home_root = Path.home() / "RootBase"
    if home_root.is_dir():
        return home_root.resolve()

    # Last resort: the package's own directory (keeps imports self-contained).
    return Path(__file__).resolve().parent


def _resolve_monitored_paths() -> List[str]:
    """Return RELATIVE paths (to ROOT_DIR) to monitor; [] = whole ROOT_DIR."""
    env = os.environ.get("TRUTHSLEUTH_PATHS", "")
    if env.strip():
        return [p.strip() for p in env.split(",") if p.strip()]
    # Default: monitor the whole ROOT_DIR (Android-era data_scouts/ no longer exists).
    return []


def _resolve_molt_engine() -> Optional[Path]:
    """Resolve the gray-hat Molt engine entry point, or None if unavailable."""
    env = os.environ.get("TRUTHSLEUTH_MOLT_ENGINE")
    if env:
        p = Path(env).expanduser()
        return p if p.exists() else None

    # 1) Canonical molt_v3 engine (restored into ROOT_DIR from recovery).
    p = ROOT_DIR / "molt_v3_engine" / "molt_v3.py"
    if p.exists():
        return p.resolve()

    # 2) Live working OpenRouter shim (MikeySwarm ox_package).
    p = Path.home() / "MikeySwarm" / "agents" / "ox_package" / "molt"
    if p.exists():
        return p.resolve()

    return None


def _molt_engine_kind(engine: Optional[Path]) -> Optional[str]:
    """Classify the resolved engine so dispatch can adapt its CLI args."""
    if engine is None:
        return None
    if engine.name == "molt_v3.py":
        return "molt_v3"
    return "shim"


# Root directory of the monitored project (Crostini: ~/RootBase).
ROOT_DIR = _resolve_root_dir()

# Directories/files to exclude from monitoring (glob patterns relative to ROOT_DIR).
EXCLUSION_PATTERNS = [
    "molt_engine/**",
    "molt_v3_engine/**",
    "data/motherbrain/api/bus/**",
    "node_modules/**",
    ".git/**",
    "__pycache__/**",
    "*.pyc",
    "*.txt",
    "*.md",
    "archive/**",
    "tmp/**",
    "bin/**",
    "nemo/**",
    "ollama_models_too/**",
    "swarm_intell_dupe",
    "structure_dump.txt",
]

# Paths to explicitly monitor (relative to ROOT_DIR). Empty = whole ROOT_DIR.
MONITORED_PATHS: List[str] = _resolve_monitored_paths()

# Reporting configuration.
REPORTING_CONFIG = {
    "output_format": "json",  # or "text", "markdown"
    "report_file": ROOT_DIR / "logs" / "truthsleuth_report.json",
}

# Thresholds and rules for code quality.
CODE_QUALITY_RULES = {
    "max_line_length": 100,
    "max_function_complexity": 10,  # Cyclomatic complexity
    "forbidden_patterns": [
        "eval(",
        "exec(",
    ],
    "min_docstring_length": 20,  # Minimum characters for a docstring
}

# Gray-hat Molt engine (resolved at import time).
MOLT_ENGINE = _resolve_molt_engine()
MOLT_ENGINE_KIND = _molt_engine_kind(MOLT_ENGINE)
