"""Tests for filter_helpers module."""
import pytest

from src.data.filter_engine import FilterSet, CategoryFilter, DateRangeFilter
from src.utils.filter_helpers import build_filter_set_from_map


class TestBuildFilterSetFromMap:
    """build_filter_set_from_map must construct FilterSet correctly."""

    def test_empty_filter_pairs_returns_empty_filterset(self):
        column_map = {"month": "Delivery Month", "area": "Area"}
        filters = build_filter_set_from_map(column_map, [])
        assert isinstance(filters, FilterSet)
        assert len(filters.category_filters) == 0
        assert len(filters.date_filters) == 0

    def test_single_category_filter(self):
        column_map = {"month": "Delivery Month"}
        filters = build_filter_set_from_map(
            column_map,
            [("month", ["2024-01", "2024-02"])],
        )
        assert len(filters.category_filters) == 1
        assert filters.category_filters[0].column == "Delivery Month"
        assert filters.category_filters[0].values == ["2024-01", "2024-02"]

    def test_multiple_category_filters(self):
        column_map = {
            "month": "Delivery Month",
            "area": "Area",
            "category": "Category",
        }
        filters = build_filter_set_from_map(
            column_map,
            [
                ("month", ["2024-01"]),
                ("area", ["APAC", "EMEA"]),
                ("category", ["WS-A"]),
            ],
        )
        assert len(filters.category_filters) == 3
        assert filters.category_filters[0].column == "Delivery Month"
        assert filters.category_filters[1].column == "Area"
        assert filters.category_filters[2].column == "Category"

    def test_none_values_skipped(self):
        column_map = {"month": "Delivery Month", "area": "Area"}
        filters = build_filter_set_from_map(
            column_map,
            [("month", ["2024-01"]), ("area", None)],
        )
        assert len(filters.category_filters) == 1
        assert filters.category_filters[0].column == "Delivery Month"

    def test_empty_list_values_skipped(self):
        column_map = {"month": "Delivery Month", "area": "Area"}
        filters = build_filter_set_from_map(
            column_map,
            [("month", []), ("area", ["APAC"])],
        )
        assert len(filters.category_filters) == 1
        assert filters.category_filters[0].column == "Area"

    def test_unknown_key_skipped(self):
        column_map = {"month": "Delivery Month"}
        filters = build_filter_set_from_map(
            column_map,
            [("month", ["2024-01"]), ("unknown_key", ["value"])],
        )
        assert len(filters.category_filters) == 1
        assert filters.category_filters[0].column == "Delivery Month"

    def test_date_range_filter(self):
        column_map = {"date": "Created Date"}
        filters = build_filter_set_from_map(
            column_map,
            [],
            date_range=("date", "2024-01-01", "2024-01-31"),
        )
        assert len(filters.date_filters) == 1
        assert filters.date_filters[0].column == "Created Date"
        assert filters.date_filters[0].start_date == "2024-01-01"
        assert filters.date_filters[0].end_date == "2024-01-31"

    def test_date_range_none_skipped(self):
        column_map = {"date": "Created Date"}
        filters = build_filter_set_from_map(
            column_map,
            [],
            date_range=("date", None, "2024-01-31"),
        )
        assert len(filters.date_filters) == 0

    def test_date_range_unknown_key_skipped(self):
        column_map = {"month": "Delivery Month"}
        filters = build_filter_set_from_map(
            column_map,
            [],
            date_range=("unknown_date", "2024-01-01", "2024-01-31"),
        )
        assert len(filters.date_filters) == 0

    def test_category_and_date_filters_combined(self):
        column_map = {"month": "Delivery Month", "date": "Created Date"}
        filters = build_filter_set_from_map(
            column_map,
            [("month", ["2024-01"])],
            date_range=("date", "2024-01-01", "2024-01-31"),
        )
        assert len(filters.category_filters) == 1
        assert len(filters.date_filters) == 1
