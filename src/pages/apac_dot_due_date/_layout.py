"""Layout builder for APAC DOT Due Date Dashboard.

Extracts the page layout construction from __init__.layout() into a
standalone, testable function.
"""
from dash import html
import dash_bootstrap_components as dbc

from src.data.parquet_reader import ParquetReader
from src.data.data_source_registry import get_dataset_id
from ._constants import DASHBOARD_ID, CHART_ID_REFERENCE_TABLE, DATASET_ID
from ._data_loader import load_filter_options
from ._filters import build_filter_layout


def build_layout() -> html.Div:
    """Build the full APAC DOT Due Date Dashboard layout.

    Returns:
        html.Div containing:
            - H1 page title
            - Filter panel (5 rows via build_filter_layout)
            - Chart/table section (table-title + apac-table)
    """
    # Load data to get available options for filters
    reader = ParquetReader()
    dataset_id = get_dataset_id(DASHBOARD_ID, CHART_ID_REFERENCE_TABLE) or DATASET_ID
    opts = load_filter_options(reader, dataset_id)

    # Build filter rows via _filters module
    filter_rows = build_filter_layout(opts)

    return html.Div([
        html.H1("APAC DOT Due Date Dashboard", className="mb-4"),

        # Filter rows (control, month, prc, category, additional)
        *filter_rows,

        # Reference / Table Section
        dbc.Row([
            dbc.Col([
                html.H3(id="apac-dot-chart-00-title", className="mt-4 mb-3"),
                html.Div(id="apac-dot-chart-00"),
            ], md=12),
        ]),
    ], className="page-container")
