"""Pydantic models for business requirements."""
from typing import List, Optional
from pydantic import BaseModel, Field


class Requirement(BaseModel):
    """A single business requirement extracted from a transcript."""

    id: str = Field(description="Unique requirement ID in format REQ-XXX")
    statement: str = Field(description="Concise requirement statement")
    priority: str = Field(
        description="Priority level: must-have, nice-to-have, or unclear"
    )
    constraints: List[str] = Field(
        default_factory=list,
        description="Constraints, conditions, SLAs, compliance rules"
    )
    raised_by: str = Field(description="Speaker or role who raised it")
    implicit: bool = Field(
        default=False,
        description="True if requirement is implied rather than explicit"
    )
    source_transcript: str = Field(
        default="",
        description="Source transcript filename"
    )


class RequirementsList(BaseModel):
    """Collection of extracted requirements."""

    requirements: List[Requirement] = Field(
        default_factory=list,
        description="List of extracted requirements"
    )
