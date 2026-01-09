"""Utah SB60 income tax reduction analysis package."""

from .reform import ut_sb60_reform
from .household import calculate_net_income_changes
from .statewide import (
    DECILES,
    GAIN_MORE_THAN_5PCT,
    GAIN_LESS_THAN_5PCT,
    NO_CHANGE,
    LOSS_LESS_THAN_5PCT,
    LOSS_MORE_THAN_5PCT,
    ALL_GAIN_MORE_THAN_5PCT,
    ALL_GAIN_LESS_THAN_5PCT,
    ALL_NO_CHANGE,
    ALL_LOSS_LESS_THAN_5PCT,
    ALL_LOSS_MORE_THAN_5PCT,
    AVG_IMPACT_BY_DECILE,
    REVENUE_IMPACT_MILLIONS,
    PERCENT_BENEFITING,
    POVERTY_IMPACT_PCT,
    DEEP_POVERTY_IMPACT_PCT,
    GINI_IMPACT_PCT,
    AVG_BENEFIT_PER_HOUSEHOLD,
)
from .charts import (
    create_net_income_change_chart,
    create_winners_by_decile_chart,
    create_avg_benefit_by_decile_chart,
)

__all__ = [
    # Reform
    "ut_sb60_reform",
    # Household calculations
    "calculate_net_income_changes",
    # Statewide data
    "DECILES",
    "GAIN_MORE_THAN_5PCT",
    "GAIN_LESS_THAN_5PCT",
    "NO_CHANGE",
    "LOSS_LESS_THAN_5PCT",
    "LOSS_MORE_THAN_5PCT",
    "ALL_GAIN_MORE_THAN_5PCT",
    "ALL_GAIN_LESS_THAN_5PCT",
    "ALL_NO_CHANGE",
    "ALL_LOSS_LESS_THAN_5PCT",
    "ALL_LOSS_MORE_THAN_5PCT",
    "AVG_IMPACT_BY_DECILE",
    "REVENUE_IMPACT_MILLIONS",
    "PERCENT_BENEFITING",
    "POVERTY_IMPACT_PCT",
    "DEEP_POVERTY_IMPACT_PCT",
    "GINI_IMPACT_PCT",
    "AVG_BENEFIT_PER_HOUSEHOLD",
    # Charts
    "create_net_income_change_chart",
    "create_winners_by_decile_chart",
    "create_avg_benefit_by_decile_chart",
]
