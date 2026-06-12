"""Pydantic models for gap analysis output."""
from typing import List, Optional
from pydantic import BaseModel, Field


class Gap(BaseModel):
    """A single gap identified between requirements and solutions."""

    gap_id: str = Field(description="Unique gap ID in format GAP-XXX")
    type: str = Field(
        description="Gap type: unaddressed, scope_mismatch, implicit_assumption, or ambiguity"
    )
    requirement_refs: List[str] = Field(
        default_factory=list,
        description="Requirement IDs this gap relates to"
    )
    solution_refs: List[str] = Field(
        default_factory=list,
        description="Solution IDs this gap relates to"
    )
    description: str = Field(
        description="Plain-English description of the gap"
    )
    severity: str = Field(
        description="Severity: high, medium, or low"
    )
    suggested_action: str = Field(
        description="Specific question or action to resolve the gap"
    )


class GapReport(BaseModel):
    """Complete gap analysis report."""

    gaps: List[Gap] = Field(
        default_factory=list,
        description="List of identified gaps"
    )
