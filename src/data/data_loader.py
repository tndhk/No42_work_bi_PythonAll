"""Common data loader utilities for dashboards."""
from __future__ import annotations

import pandas as pd

from src.core.cache import get_cached_dataset
from src.data.parquet_reader import ParquetReader
from src.data.data_source_registry import get_dataset_id


def load_dataset_for_chart(
    reader: ParquetReader, dashboard_id: str, chart_id: str
) -> pd.DataFrame:
    """Load dataset for a given chart via dashboard config."""
    dataset_id = get_dataset_id(dashboard_id, chart_id)
    if dataset_id is None:
        raise ValueError(
            f"Dataset ID not found for dashboard '{dashboard_id}' and chart '{chart_id}'"
        )
    return get_cached_dataset(reader, dataset_id)
