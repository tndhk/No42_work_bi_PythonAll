"""Tests for common dashboard data loader."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pandas as pd
import pytest


@patch("src.data.data_loader.get_cached_dataset")
@patch("src.data.data_loader.get_dataset_id")
def test_load_dataset_for_chart_uses_resolved_dataset(
    mock_get_dataset_id, mock_get_cached
):
    from src.data.data_loader import load_dataset_for_chart

    df = pd.DataFrame({"a": [1, 2]})
    mock_get_dataset_id.return_value = "dataset-1"
    mock_get_cached.return_value = df

    reader = MagicMock()
    result = load_dataset_for_chart(reader, "dashboard-x", "chart-1")

    assert result is df
    mock_get_cached.assert_called_once_with(reader, "dataset-1")


@patch("src.data.data_loader.get_dataset_id")
def test_load_dataset_for_chart_missing_dataset_raises(mock_get_dataset_id):
    from src.data.data_loader import load_dataset_for_chart

    mock_get_dataset_id.return_value = None
    reader = MagicMock()

    with pytest.raises(ValueError):
        load_dataset_for_chart(reader, "dashboard-x", "chart-missing")
