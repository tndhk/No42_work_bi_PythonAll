"""Hamm Overview dashboard page."""
import dash

from ._layout import build_layout
from . import _callbacks  # noqa: F401


dash.register_page(
    __name__,
    path="/hamm-overview",
    name="Hamm Overview",
    order=3,
    layout=build_layout,
)
