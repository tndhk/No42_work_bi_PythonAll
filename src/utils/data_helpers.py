"""Helper functions for data loading and dataset resolution."""
from typing import Callable, Optional, Dict, List
import pandas as pd

from src.data.parquet_reader import ParquetReader
from src.core.cache import get_cached_dataset
from src.data.filter_engine import extract_unique_values
from src.data.data_source_registry import resolve_dataset_id


def safe_load_filter_options(
    reader: ParquetReader,
    dataset_id: str,
    extract_columns: Dict[str, str],
    prepare_fn: Optional[Callable[[pd.DataFrame], pd.DataFrame]] = None,
) -> Dict[str, List]:
    """Load unique values from specified columns in a dataset, with safe defaults.

    Args:
        reader: ParquetReader instance.
        dataset_id: Dataset identifier.
        extract_columns: Mapping from output key to DataFrame column name.
            Example: {"months": "Delivery Month", "areas": "Area"}
        prepare_fn: Optional function to prepare DataFrame before extraction.
            Example: strip_timezone, add derived columns, etc.

    Returns:
        Dictionary with keys from extract_columns and lists of unique values.
        On exception, returns empty lists for all keys.

    Example:
        >>> reader = ParquetReader()
        >>> opts = safe_load_filter_options(
        ...     reader,
        ...     "my-dataset",
        ...     {"months": "Delivery Month", "areas": "Area"},
        ... )
        >>> "months" in opts
        True
        >>> isinstance(opts["months"], list)
        True
    """
    try:
        df = get_cached_dataset(reader, dataset_id)

        if prepare_fn:
            df = prepare_fn(df)

        result = {}
        for key, column_name in extract_columns.items():
            result[key] = extract_unique_values(df, column_name)

        return result

    except Exception:
        # Return safe defaults: empty lists for all keys
        return {key: [] for key in extract_columns.keys()}


def strip_timezone(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Convert a timezone-aware datetime column to timezone-naive.

    Parquet files often store timestamps as UTC-aware, but filter_engine
    expects timezone-naive Timestamps for comparison.

    Args:
        df: DataFrame to modify (will be copied).
        column: Column name to convert.

    Returns:
        DataFrame with the specified column converted to timezone-naive.

    Example:
        >>> df = pd.DataFrame({"date": pd.date_range("2024-01-01", periods=3, tz="UTC")})
        >>> df["date"].dtype
        datetime64[ns, UTC]
        >>> df_naive = strip_timezone(df, "date")
        >>> df_naive["date"].dtype
        datetime64[ns]
    """
    df = df.copy()
    if column in df.columns:
        df[column] = pd.to_datetime(df[column], utc=True).dt.tz_convert(None)
    return df


def resolve_single_dataset_id(dashboard_id: str, chart_ids: List[str]) -> str:
    """Resolve dataset ID for a dashboard, ensuring all charts use the same dataset.

    Validates that all chart IDs in the dashboard map to exactly one dataset ID.
    This is useful for dashboards where all charts should use the same data source.

    Args:
        dashboard_id: Dashboard identifier.
        chart_ids: List of chart IDs to check.

    Returns:
        The single dataset ID that all charts map to.

    Raises:
        ValueError: If charts map to multiple different dataset IDs.

    Example:
        >>> chart_ids = ["chart-1", "chart-2", "chart-3"]
        >>> dataset_id = resolve_single_dataset_id("my_dashboard", chart_ids)
        >>> isinstance(dataset_id, str)
        True
    """
    dataset_ids = {resolve_dataset_id(dashboard_id, chart_id) for chart_id in chart_ids}
    if len(dataset_ids) != 1:
        raise ValueError(
            f"Multiple dataset IDs found for dashboard '{dashboard_id}': "
            f"{sorted(dataset_ids)}. All charts must use the same dataset."
        )
    return next(iter(dataset_ids))
