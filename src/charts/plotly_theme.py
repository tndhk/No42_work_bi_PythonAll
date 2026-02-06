"""Custom Plotly theme for Warm Professional light theme."""
import plotly.graph_objects as go

# Color palette for Warm Professional light theme
PLOTLY_COLOR_PALETTE = [
    "#2563eb",  # Blue (primary)
    "#059669",  # Emerald
    "#d97706",  # Amber
    "#dc2626",  # Red
    "#7c3aed",  # Violet
    "#0891b2",  # Cyan
]

# Plotly template configuration
PLOTLY_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        # Colors
        colorway=PLOTLY_COLOR_PALETTE,
        paper_bgcolor="rgba(0,0,0,0)",  # Transparent to match card background
        plot_bgcolor="rgba(0,0,0,0)",  # Transparent
        
        # Fonts
        font=dict(
            family="Noto Sans JP, Inter, sans-serif",
            size=12,
            color="#64748b",
        ),
        title=dict(
            font=dict(
                family="Noto Sans JP, Inter, sans-serif",
                size=18,
                color="#1a1a2e",
            ),
        ),
        
        # Axes
        xaxis=dict(
            gridcolor="#e2e8f0",
            gridwidth=1,
            linecolor="#e2e8f0",
            zeroline=False,
            tickfont=dict(color="#64748b"),
            title=dict(font=dict(color="#1a1a2e", family="Noto Sans JP, Inter, sans-serif")),
        ),
        yaxis=dict(
            gridcolor="#e2e8f0",
            gridwidth=1,
            linecolor="#e2e8f0",
            zeroline=False,
            tickfont=dict(color="#64748b"),
            title=dict(font=dict(color="#1a1a2e", family="Noto Sans JP, Inter, sans-serif")),
        ),
        
        # Legend
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor="#e2e8f0",
            borderwidth=1,
            font=dict(color="#64748b", family="Noto Sans JP, Inter, sans-serif"),
        ),
        
        # Hover
        hovermode="closest",
        hoverlabel=dict(
            bgcolor="#ffffff",
            bordercolor="rgba(37, 99, 235, 0.3)",
            font=dict(color="#1a1a2e", family="Noto Sans JP, Inter, sans-serif"),
        ),
    )
)


def apply_theme(fig: go.Figure) -> go.Figure:
    """Apply custom theme to a Plotly figure.
    
    Args:
        fig: Plotly figure to style
        
    Returns:
        Styled figure
    """
    fig.update_layout(template=PLOTLY_TEMPLATE)
    return fig
