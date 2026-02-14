def calculate_green_score(total_operation_weight: float) -> float:
    """
    Converts total operation weight into normalized green score (0 - 100)
    """

    penalty_factor = 0.6   # Tunable constant

    effective_penalty = total_operation_weight * penalty_factor
    score = 100 - effective_penalty

    return max(0, round(score, 2))
