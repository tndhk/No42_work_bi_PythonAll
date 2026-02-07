"""Tests for Hamm Overview constants module."""


class TestDatasetId:
    def test_dataset_id_value(self):
        from src.pages.hamm_overview._constants import DATASET_ID

        assert DATASET_ID == "hamm-dashboard"


class TestDashboardId:
    def test_dashboard_id_value(self):
        from src.pages.hamm_overview._constants import DASHBOARD_ID

        assert DASHBOARD_ID == "hamm_overview"


class TestIdPrefix:
    def test_id_prefix_value(self):
        from src.pages.hamm_overview._constants import ID_PREFIX

        assert ID_PREFIX == "hamm-"


class TestColumnMap:
    def test_column_map_has_expected_keys(self):
        from src.pages.hamm_overview._constants import COLUMN_MAP

        expected = {
            "id",
            "title",
            "status",
            "created_at",
            "completed_at",
            "region",
            "content_type",
            "original_language",
            "dialogue",
            "genre",
            "error_code",
            "error_type",
            "video_duration",
            "audio_details",
        }
        assert set(COLUMN_MAP.keys()) == expected

    def test_column_map_values_are_strings(self):
        from src.pages.hamm_overview._constants import COLUMN_MAP

        for value in COLUMN_MAP.values():
            assert isinstance(value, str)


class TestChartIds:
    def test_chart_ids_values(self):
        from src.pages.hamm_overview import _constants as const

        assert const.CHART_ID_VOLUME_TABLE == "hamm-volume-table"
        assert const.CHART_ID_VOLUME_CHART == "hamm-volume-chart"
        assert const.CHART_ID_TASK_TABLE == "hamm-task-table"
