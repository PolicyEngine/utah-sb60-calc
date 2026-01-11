# Utah SB60 Income Tax Reduction Analysis

Analysis of Utah SB60 - Income tax rate reduction from 4.5% to 4.45% in 2026.

## Key Results (2026)

- Reduces state revenues by $83.6 million
- Benefits 53.2% of Utah residents
- Has no effect on the Supplemental Poverty Measure
- Raises the Gini index of inequality by 0.01%

## Generating Blog Post Assets

```bash
pip install -e .
python generate_post.py
```

This generates:
```
output/
├── utah-sb60-income-tax-reduction.md    # Article with iframe embeds
└── charts/
    ├── net-income-change.html           # Figure 1
    ├── winners-by-decile.html           # Figure 2
    └── avg-benefit-by-decile.html       # Figure 3
```

## Copying to policyengine-app-v2

```bash
# Markdown file
cp output/utah-sb60-income-tax-reduction.md \
   ../policyengine-app-v2/app/src/data/posts/articles/

# Chart HTML files
mkdir -p ../policyengine-app-v2/app/public/charts/utah-sb60-income-tax-reduction
cp output/charts/*.html \
   ../policyengine-app-v2/app/public/charts/utah-sb60-income-tax-reduction/
```

## Package Structure

```
utah-sb60-calc/
├── utah_sb60/           # Python package
│   ├── __init__.py      # Public API exports
│   ├── reform.py        # SB60 reform definition
│   ├── household.py     # Household impact calculations
│   ├── statewide.py     # Statewide impact data
│   └── charts.py        # Chart generation functions
├── generate_post.py     # Blog post generator
└── output/              # Generated assets (not committed)
```

## Using the Python Package

```python
from utah_sb60 import (
    ut_sb60_reform,
    create_net_income_change_chart,
    create_winners_by_decile_chart,
    create_avg_benefit_by_decile_chart,
    REVENUE_IMPACT_MILLIONS,
    PERCENT_BENEFITING,
)

# Create charts
fig1 = create_net_income_change_chart()
fig2 = create_winners_by_decile_chart()
fig3 = create_avg_benefit_by_decile_chart()
```

## License

MIT
