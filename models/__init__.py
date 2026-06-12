"""Pydantic models for structured agent outputs."""
from .requirements import Requirement, RequirementsList
from .solutions import Solution, SolutionsList
from .gaps import Gap, GapReport

__all__ = [
    "Requirement",
    "RequirementsList",
    "Solution",
    "SolutionsList",
    "Gap",
    "GapReport",
]
