"""Filter UI components."""
from typing import Optional
from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc


def create_category_filter(
    filter_id: str,
    column_name: str,
    options: list[str],
    multi: bool = True,
) -> dbc.Card:
    """
    Create a category filter (Dropdown) component.

    Args:
        filter_id: Component ID (for callbacks)
        column_name: Target column name (for label display)
        options: List of options
        multi: Allow multiple selection

    Returns:
        Card-wrapped filter component
    """
    return dbc.Card([
        dbc.CardHeader(column_name, className="filter-header"),
        dbc.CardBody([
            dcc.Dropdown(
                id=filter_id,
                options=[{"label": opt, "value": opt} for opt in options],
                multi=multi,
                placeholder=f"Select {column_name}...",
            ),
        ]),
    ], className="filter-card mb-3")


def create_date_range_filter(
    filter_id: str,
    column_name: str,
    min_date: Optional[str] = None,
    max_date: Optional[str] = None,
) -> dbc.Card:
    """
    Create a date range filter (DatePickerRange) component.

    Args:
        filter_id: Component ID (for callbacks)
        column_name: Target column name (for label display)
        min_date: Minimum selectable date (ISO 8601)
        max_date: Maximum selectable date (ISO 8601)

    Returns:
        Card-wrapped filter component
    """
    return dbc.Card([
        dbc.CardHeader(column_name, className="filter-header"),
        dbc.CardBody([
            dcc.DatePickerRange(
                id=filter_id,
                min_date_allowed=min_date,
                max_date_allowed=max_date,
                start_date=min_date,
                end_date=max_date,
                display_format="YYYY-MM-DD",
            ),
        ]),
    ], className="filter-card mb-3")


def create_slicer_filter(
    filter_id: str,
    column_name: str,
    options: list[str],
    multi: bool = True,
    default_value: Optional[list[str]] = None,
) -> dbc.Card:
    """
    Create a slicer-style filter using Mantine ChipGroup.

    Args:
        filter_id: Component ID (for callbacks)
        column_name: Target column name (for label display)
        options: List of options
        multi: Allow multiple selection (default True)
        default_value: Default selected values

    Returns:
        Card-wrapped slicer filter component
    """
    chips = [
        dmc.Chip(opt, value=opt, size="sm", variant="outline")
        for opt in options
    ]

    return dbc.Card([
        dbc.CardHeader(column_name, className="filter-header"),
        dbc.CardBody([
            dmc.ChipGroup(
                id=filter_id,
                children=chips,
                value=default_value or [],
                multiple=multi,
            ),
        ]),
    ], className="filter-card slicer-filter mb-3")
