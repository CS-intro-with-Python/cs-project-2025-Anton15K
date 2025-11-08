"""Difficulty estimation utilities."""
from __future__ import annotations

from collections.abc import Iterable
from statistics import median

import numpy as np


def estimate_difficulty(ratings: Iterable[int]) -> int:
    """Estimate a difficulty rating from a collection of solver ratings.

    Uses a trimmed mean blended with the median to reduce the impact of outliers.
    """
    ratings_list = [rating for rating in ratings if rating is not None]
    if not ratings_list:
        raise ValueError("Cannot estimate difficulty from an empty rating set")

    sorted_ratings = np.sort(ratings_list)
    trim_ratio = 0.1 if len(sorted_ratings) >= 10 else 0.0
    lower_idx = int(len(sorted_ratings) * trim_ratio)
    upper_idx = int(len(sorted_ratings) * (1 - trim_ratio))
    trimmed = sorted_ratings[lower_idx:upper_idx] if trim_ratio else sorted_ratings

    trimmed_mean = float(np.mean(trimmed))
    med = median(trimmed)
    blended = 0.6 * trimmed_mean + 0.4 * med
    return int(round(blended))
