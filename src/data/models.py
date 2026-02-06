"""Data models for dataset schema."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class ColumnSchema:
    """Schema definition for a dataset column."""

    name: str
    data_type: str
    nullable: bool = False
    description: Optional[str] = None
