"""Tests for Hamm Overview data_sources.yml and dataset mapping."""
from unittest.mock import call, patch

from src.data.data_source_registry import load_dashboard_config
from src.pages.hamm_overview import _constants as const


def test_data_sources_contains_all_chart_ids():
    load_dashboard_config.cache_clear()
    config = load_dashboard_config(const.DASHBOARD_ID)
    chart_ids = set(config["charts"].keys())
    expected = {
        const.CHART_ID_VOLUME_TABLE,
        const.CHART_ID_VOLUME_CHART,
        const.CHART_ID_TASK_TABLE,
    }
    assert chart_ids == expected


@patch("src.pages.hamm_overview._data_loader.resolve_dataset_id")
def test_resolve_dataset_id_for_dashboard_uses_all_chart_ids(mock_resolve):
    from src.pages.hamm_overview._data_loader import resolve_dataset_id_for_dashboard

    mock_resolve.return_value = "hamm-dashboard"

    result = resolve_dataset_id_for_dashboard()

    assert result == "hamm-dashboard"
    expected_calls = [
        call(const.DASHBOARD_ID, const.CHART_ID_VOLUME_TABLE),
        call(const.DASHBOARD_ID, const.CHART_ID_VOLUME_CHART),
        call(const.DASHBOARD_ID, const.CHART_ID_TASK_TABLE),
    ]
    mock_resolve.assert_has_calls(expected_calls, any_order=True)
    assert mock_resolve.call_count == len(expected_calls)
