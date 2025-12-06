import math
import statistics

def estimate_problem_difficulty(solvers_data):
    """
    Estimates problem difficulty based on the average rating of all solvers.
    solvers_data: list of {'handle': str, 'net_time': int, 'rating': int, 'solve_time': int}
    """
    if not solvers_data:
        return 1500
    
    ratings = [s['rating'] for s in solvers_data if 'rating' in s]
    
    if not ratings:
        return 1500
        
    return int(statistics.mean(ratings))


def calculate_performance_rating(user_time, solvers_data):
    """
    Regression-based performance rating calculation.
    
    Model: log(net_time) = a + b * rating
    Given user's time, find rating R' where E[log(time)|R'] = log(user_time)
    
    Args:
        user_time: User's net time in seconds
        solvers_data: List of {'net_time', 'rating'}
    
    Returns:
        int: Estimated performance rating
    """
    if not solvers_data or user_time <= 0:
        return 1500
    
    # Filter valid data points
    valid_points = [(s['net_time'], s['rating']) for s in solvers_data 
                    if s.get('net_time', 0) > 0 and s.get('rating')]
    
    if len(valid_points) < 5:
        # Not enough data for regression, fall back to nearest neighbors
        return _fallback_nearest_neighbors(user_time, solvers_data)
    
    # Perform linear regression: log(time) ~ rating
    log_times = [math.log(time) for time, rating in valid_points]
    ratings = [rating for time, rating in valid_points]
    
    n = len(valid_points)
    mean_log_time = statistics.mean(log_times)
    mean_rating = statistics.mean(ratings)
    
    # Calculate slope (b) and intercept (a)
    numerator = sum((ratings[i] - mean_rating) * (log_times[i] - mean_log_time) 
                    for i in range(n))
    denominator = sum((ratings[i] - mean_rating) ** 2 for i in range(n))
    
    if denominator == 0:
        return _fallback_nearest_neighbors(user_time, solvers_data)
    
    b = numerator / denominator
    a = mean_log_time - b * mean_rating
    
    # Invert: performance_rating = (log(user_time) - a) / b
    if b == 0:
        return _fallback_nearest_neighbors(user_time, solvers_data)
    
    log_user_time = math.log(user_time)
    performance_rating = (log_user_time - a) / b
    
    # Clamp to reasonable bounds
    performance_rating = max(800, min(3500, performance_rating))
    
    return int(performance_rating)


def _fallback_nearest_neighbors(user_time, solvers_data, k=50):
    """Fallback method: average rating of k nearest neighbors by time."""
    valid_solvers = [s for s in solvers_data if s.get('net_time', 0) > 0 and s.get('rating')]
    
    if not valid_solvers:
        return 1500
    
    # Sort by time difference
    valid_solvers.sort(key=lambda x: abs(x['net_time'] - user_time))
    
    # Take top k closest
    closest = valid_solvers[:min(k, len(valid_solvers))]
    
    if not closest:
        return 1500
    
    return int(statistics.mean(s['rating'] for s in closest))


def calculate_time_percentile(user_time, solvers_data):
    """
    Calculate what percentile the user's time falls into.
    0 = fastest, 100 = slowest
    """
    if not solvers_data:
        return 50.0
    
    times = sorted([s['net_time'] for s in solvers_data if s.get('net_time', 0) > 0])
    
    if not times:
        return 50.0
    
    # Count how many are faster than user
    faster_count = sum(1 for t in times if t < user_time)
    
    percentile = (faster_count / len(times)) * 100
    return percentile


def calculate_actual_performance_score(time_percentile):
    """
    Convert time percentile to a performance score (0-1).
    
    Faster times (low percentile) = higher score
    Slower times (high percentile) = lower score
    
    Using a sigmoid-like mapping:
    - Top 1% (percentile 0-1): score ~0.99
    - Top 10% (percentile 0-10): score ~0.9
    - Median (percentile 50): score 0.5
    - Bottom 10% (percentile 90-100): score ~0.1
    """
    # Invert percentile so lower time = higher score
    # Map [0, 100] to [1, 0]
    return 1.0 - (time_percentile / 100.0)


def calculate_expected_performance_score(user_rating, problem_rating):
    """
    Elo-inspired expected score calculation.
    
    If user rating = problem rating, expected score = 0.5
    If user rating > problem rating, expected score > 0.5
    If user rating < problem rating, expected score < 0.5
    
    Formula: 1 / (1 + 10^((problem_rating - user_rating) / 400))
    """
    if user_rating is None or problem_rating is None:
        return 0.5
    
    exponent = (problem_rating - user_rating) / 400.0
    expected = 1.0 / (1.0 + math.pow(10, exponent))
    
    return expected


def calculate_rating_delta(user_rating, performance_rating, expected_score, actual_score, k_factor=32):
    """
    Calculate rating delta based on expected vs actual performance.
    
    Args:
        user_rating: User's current rating
        performance_rating: Rating implied by solve time
        expected_score: Expected performance (0-1) based on user/problem rating
        actual_score: Actual performance (0-1) based on time percentile
        k_factor: Sensitivity parameter (higher = larger swings)
    
    Returns:
        int: Rating delta (positive = performed better than expected)
    """
    if user_rating is None:
        return 0
    
    # Elo-style delta
    base_delta = k_factor * (actual_score - expected_score)
    
    # Scale by the magnitude of performance vs user rating
    # If you performed way better/worse than your rating, delta should be larger
    performance_diff = performance_rating - user_rating
    scale_factor = 1 + abs(performance_diff) / 400.0
    
    delta = base_delta * scale_factor
    
    return int(delta)


def update_problem_rating_bayesian(problem, all_attempts):
    """
    Update problem rating using Bayesian approach with confidence weighting.
    
    Args:
        problem: Problem object with initial_estimated_rating
        all_attempts: List of Attempt objects with performance_rating and user.rating
    
    Returns:
        tuple: (new_rating, confidence)
    """
    if not all_attempts:
        initial = problem.initial_estimated_rating or 1500
        return initial, 0.3  # Low confidence
    
    # Prior from Codeforces data
    prior = problem.initial_estimated_rating or 1500
    prior_weight = 10  # Strong prior
    
    # Calculate weighted performances
    weighted_performances = []
    total_weight = 0
    
    for attempt in all_attempts:
        if attempt.performance_rating is None:
            continue
        
        # Weight by solver rating (higher rated = more reliable)
        user_rating = attempt.user.rating if attempt.user and attempt.user.rating else 1500
        rating_weight = 1.0 + (user_rating / 2000.0)
        
        # Diminishing returns as we get more data
        data_count = len(all_attempts)
        data_weight = 1.0 / math.sqrt(1 + data_count)
        
        combined_weight = rating_weight * data_weight
        
        weighted_performances.append(attempt.performance_rating * combined_weight)
        total_weight += combined_weight
    
    if total_weight == 0:
        return prior, 0.3
    
    # Bayesian posterior
    sum_weighted_perf = sum(weighted_performances)
    posterior = (prior * prior_weight + sum_weighted_perf) / (prior_weight + total_weight)
    
    # Confidence increases with more data, but asymptotes
    # Ranges from ~0.3 (no data) to ~0.95 (lots of data)
    confidence = 0.3 + 0.65 * (1 - math.exp(-len(all_attempts) / 10.0))
    
    return int(posterior), confidence
