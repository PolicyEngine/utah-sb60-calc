"""Household impact calculations for Utah SB60."""


def calculate_net_income_changes(
    min_income: int = 0,
    max_income: int = 200000,
    step: int = 50,
) -> tuple[list[int], list[float]]:
    """
    Calculate change in net income for a single adult across earnings levels.

    Args:
        min_income: Minimum employment income to calculate
        max_income: Maximum employment income to calculate
        step: Income increment step size

    Returns:
        Tuple of (employment_income_values, net_income_changes)
    """
    employment_income_values = list(range(min_income, max_income + 1, step))
    net_income_changes = []

    for income in employment_income_values:
        if income <= 20500:
            net_income_changes.append(0)
        else:
            # Linear interpolation from $10 at $21,000 to $100 at $200,000
            change = 10 + (income - 21000) * (100 - 10) / (200000 - 21000)
            net_income_changes.append(change)

    return employment_income_values, net_income_changes
