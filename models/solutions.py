"""Pydantic models for engineering solutions."""
from typing import List, Optional
from pydantic import BaseModel, Field


class Solution(BaseModel):
    """A single engineering solution/decision extracted from a transcript."""

    id: str = Field(description="Unique solution ID in format SOL-XXX")
    statement: str = Field(description="What is being built or decided")
    scope_limitations: List[str] = Field(
        default_factory=list,
        description="Explicit scope limitations vs what might be expected"
    )
    technologies: List[str] = Field(
        default_factory=list,
        description="Technologies or tools mentioned"
    )
    deferred: List[str] = Field(
        default_factory=list,
        description="Items explicitly pushed to later phases"
    )
    assumptions: List[str] = Field(
        default_factory=list,
        description="Assumptions engineers are making"
    )
    source_transcript: str = Field(
        default="",
        description="Source transcript filename"
    )


class SolutionsList(BaseModel):
    """Collection of extracted solutions."""

    solutions: List[Solution] = Field(
        default_factory=list,
        description="List of extracted solutions"
    )
