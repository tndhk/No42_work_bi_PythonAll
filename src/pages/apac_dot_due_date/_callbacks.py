"""Dash callbacks for APAC DOT Due Date Dashboard page.

Extracted from __init__.py to separate callback registration from page
registration.  Importing this module triggers callback registration via
the ``@callback`` decorator as a side effect.
"""
from dash import callback, html, Input, Output

from src.data.parquet_reader import ParquetReader
from src.data.data_source_registry import get_dataset_id
from ._constants import DASHBOARD_ID, CHART_ID_REFERENCE_TABLE, DATASET_ID
from ._data_loader import load_and_filter_data
from .charts import _ch00_reference_table


@callback(
    [
        Output("apac-dot-chart-00-title", "children"),
        Output("apac-dot-chart-00", "children"),
    ],
    [
        Input("apac-dot-ctrl-num-percent", "value"),
        Input("apac-dot-ctrl-breakdown", "active_tab"),
        Input("apac-dot-filter-month", "value"),
        Input("apac-dot-filter-prc", "value"),
        Input("apac-dot-filter-area", "value"),
        Input("apac-dot-filter-category", "value"),
        Input("apac-dot-filter-vendor", "value"),
        Input("apac-dot-filter-amp-av", "value"),
        Input("apac-dot-filter-order-type", "value"),
    ],
)
def update_all_charts(
    num_percent_mode,
    breakdown_tab,
    selected_months,
    prc_filter_value,
    area_values,
    category_values,
    vendor_values,
    amp_av_values,
    order_type_values,
):
    """Update all charts based on filter inputs.

    Creates a ParquetReader, calls load_and_filter_data once, and passes
    the result to _ch00_reference_table.build().
    """
    reader = ParquetReader()

    try:
        dataset_id = get_dataset_id(DASHBOARD_ID, CHART_ID_REFERENCE_TABLE) or DATASET_ID
        filtered_df = load_and_filter_data(
            reader,
            dataset_id,
            selected_months=selected_months,
            prc_filter_value=prc_filter_value,
            area_values=area_values,
            category_values=category_values,
            vendor_values=vendor_values,
            amp_av_values=amp_av_values,
            order_type_values=order_type_values,
        )

        return _ch00_reference_table.build(filtered_df, breakdown_tab, num_percent_mode)

    except Exception as e:
        error_msg = html.Div([
            html.P(f"Error loading data: {str(e)}", className="text-danger"),
        ])

        return (
            "0) Reference : Number of Work Order",
            error_msg,
        )
