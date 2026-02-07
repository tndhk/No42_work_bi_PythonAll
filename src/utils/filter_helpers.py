"""Helper functions for building FilterSet from column maps.

Reduces boilerplate when constructing FilterSet from multiple filter values.
"""
from typing import Optional, Dict, List, Tuple, Any

from src.data.filter_engine import FilterSet, CategoryFilter, DateRangeFilter


def build_filter_set_from_map(
    column_map: Dict[str, str],
    filter_pairs: List[Tuple[str, Optional[List[Any]]]],
    date_range: Optional[Tuple[str, Optional[str], Optional[str]]] = None,
) -> FilterSet:
    """Build a FilterSet from column map keys and filter value pairs.

    Args:
        column_map: Mapping from logical filter key to DataFrame column name.
            Example: {"month": "Delivery Completed Month", "area": "business area"}
        filter_pairs: List of (key, values) tuples where key is a key in column_map
            and values is a list of filter values or None/[].
            Example: [("month", selected_months), ("area", area_values), ...]
        date_range: Optional tuple of (key, start_date, end_date) for date filtering.
            start_date and end_date should be ISO 8601 strings (YYYY-MM-DD) or None.

    Returns:
        FilterSet with CategoryFilter and/or DateRangeFilter instances added.

    Example:
        >>> column_map = {"month": "Delivery Month", "area": "Area"}
        >>> filters = build_filter_set_from_map(
        ...     column_map,
        ...     [("month", ["2024-01", "2024-02"]), ("area", ["North", "South"])],
        ... )
        >>> len(filters.category_filters)
        2
    """
    filters = FilterSet()

    # Add category filters
    for key, values in filter_pairs:
        if values and key in column_map:
            filters.category_filters.append(
                CategoryFilter(column=column_map[key], values=values)
            )

    # Add date range filter if provided
    if date_range:
        key, start_date, end_date = date_range
        if start_date and end_date and key in column_map:
            filters.date_filters.append(
                DateRangeFilter(
                    column=column_map[key],
                    start_date=start_date,
                    end_date=end_date,
                )
            )

    return filters
