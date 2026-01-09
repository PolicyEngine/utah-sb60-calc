"""Statewide impact data for Utah SB60."""

# Income deciles (1-10)
DECILES = list(range(1, 11))

# Percentage of population by outcome category for each decile
GAIN_MORE_THAN_5PCT = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
GAIN_LESS_THAN_5PCT = [17.2, 7.4, 26.5, 29.7, 44.4, 72.2, 57.5, 78.3, 99.8, 99.1]
NO_CHANGE = [82.8, 92.6, 73.5, 70.3, 55.6, 27.8, 42.5, 21.7, 0.2, 0.9]
LOSS_LESS_THAN_5PCT = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
LOSS_MORE_THAN_5PCT = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Overall population totals
ALL_GAIN_MORE_THAN_5PCT = 0
ALL_GAIN_LESS_THAN_5PCT = 53.2
ALL_NO_CHANGE = 46.8
ALL_LOSS_LESS_THAN_5PCT = 0
ALL_LOSS_MORE_THAN_5PCT = 0

# Average impact by decile (in dollars)
AVG_IMPACT_BY_DECILE = [5, 12, 23, 35, 52, 84, 155, 254, 297, 583]

# Key statistics
REVENUE_IMPACT_MILLIONS = -83.6
PERCENT_BENEFITING = 53.2
POVERTY_IMPACT_PCT = 0.0
DEEP_POVERTY_IMPACT_PCT = 0.0
GINI_IMPACT_PCT = 0.01
AVG_BENEFIT_PER_HOUSEHOLD = 130
