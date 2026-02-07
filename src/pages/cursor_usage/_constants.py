"""Constants for the Cursor Usage Dashboard page.

Centralizes dataset identifiers, column name mappings, and ID prefixes
to avoid hardcoded strings scattered across layout and callback code.
"""

# Dashboard identifier (used for config lookup)
DASHBOARD_ID: str = "cursor_usage"

# S3/Parquet dataset identifier (legacy fallback)
DATASET_ID: str = "cursor-usage"

# Component ID namespace prefix (for avoiding collisions with other pages)
ID_PREFIX: str = "cu-"

# Chart IDs used in this dashboard
CHART_ID_KPI_TOTAL_COST: str = f"{ID_PREFIX}kpi-total-cost"
CHART_ID_KPI_TOTAL_TOKENS: str = f"{ID_PREFIX}kpi-total-tokens"
CHART_ID_KPI_REQUEST_COUNT: str = f"{ID_PREFIX}kpi-request-count"
CHART_ID_COST_TREND: str = f"{ID_PREFIX}chart-cost-trend"
CHART_ID_TOKEN_EFFICIENCY: str = f"{ID_PREFIX}chart-token-efficiency"
CHART_ID_MODEL_DISTRIBUTION: str = f"{ID_PREFIX}chart-model-distribution"
CHART_ID_DATA_TABLE: str = f"{ID_PREFIX}data-table"

# Mapping from logical filter/column key to the actual DataFrame column name.
# Keys are short identifiers used in code; values are the raw column names
# as they appear in the Parquet/DataFrame.
COLUMN_MAP: dict[str, str] = {
    "date": "Date",
    "model": "Model",
    "cost": "Cost",
    "total_tokens": "Total Tokens",
    "user": "User",
    "kind": "Kind",
}
