# utah-sb60-calc

Analysis of Utah SB60 - Income tax rate reduction from 4.5% to 4.45% in 2026.

## Installation

```bash
pip install -e .
```

## Usage

```python
from utah_sb60 import (
    ut_sb60_reform,
    create_net_income_change_chart,
    create_winners_by_decile_chart,
    create_avg_benefit_by_decile_chart,
    REVENUE_IMPACT_MILLIONS,
    PERCENT_BENEFITING,
)

# Access the reform definition
reform = ut_sb60_reform

# Create charts
fig1 = create_net_income_change_chart()
fig2 = create_winners_by_decile_chart()
fig3 = create_avg_benefit_by_decile_chart()

# Access key statistics
print(f"Revenue impact: ${REVENUE_IMPACT_MILLIONS} million")
print(f"Percent benefiting: {PERCENT_BENEFITING}%")
```

## Key Results (2026)

- Reduces state revenues by $83.6 million
- Benefits 53.2% of Utah residents
- Has no effect on the Supplemental Poverty Measure
- Raises the Gini index of inequality by 0.01%

## Package Structure

```
utah_sb60/
├── __init__.py      # Public API exports
├── reform.py        # SB60 reform definition
├── household.py     # Household impact calculations
├── statewide.py     # Statewide impact data
└── charts.py        # Chart generation functions
```

## License

MIT
