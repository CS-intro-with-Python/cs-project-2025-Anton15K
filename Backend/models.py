"""Simple domain data classes (structure only).

These represent the core domain entities. The project does not require
persistence yet; models are defined to provide shapes for future work.
"""

from __future__ import annotations

from .entities import User, Problem, Attempt, RatingAdjustment

__all__ = [
    "User",
    "Problem",
    "Attempt",
    "RatingAdjustment",
]
