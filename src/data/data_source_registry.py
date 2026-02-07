"""Registry for mapping dashboard/chart IDs to dataset IDs via YAML configs."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml


DASHBOARD_PAGES_DIR = Path(__file__).resolve().parents[1] / "pages"
DASHBOARD_CONFIG_FILENAME = "data_sources.yml"


def _config_path(dashboard_id: str) -> Path:
    return DASHBOARD_PAGES_DIR / dashboard_id / DASHBOARD_CONFIG_FILENAME


@lru_cache(maxsize=128)
def load_dashboard_config(dashboard_id: str) -> dict[str, Any]:
    """Load YAML config for a dashboard.

    Raises:
        FileNotFoundError: If the config file does not exist.
        ValueError: If YAML structure is invalid.
    """
    path = _config_path(dashboard_id)
    if not path.exists():
        raise FileNotFoundError(f"Dashboard config not found: {path}")

    data = yaml.safe_load(path.read_text()) or {}
    if not isinstance(data, dict):
        raise ValueError("Dashboard config must be a mapping")

    charts = data.get("charts", {})
    if not isinstance(charts, dict):
        raise ValueError("Dashboard config 'charts' must be a mapping")

    return {"charts": charts}


def get_dataset_id(dashboard_id: str, chart_id: str) -> str | None:
    """Resolve dataset_id for a chart in a dashboard config.

    Returns:
        dataset_id string if found, otherwise None.
    """
    config = load_dashboard_config(dashboard_id)
    charts = config.get("charts", {})
    if not isinstance(charts, dict):
        return None

    dataset_id = charts.get(chart_id)
    if isinstance(dataset_id, str):
        return dataset_id
    return None
