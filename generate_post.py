#!/usr/bin/env python3
"""
Generate blog post assets for Utah SB60 analysis.

This script generates:
1. A markdown file with iframe embeds pointing to GitHub Pages
2. Standalone HTML files for each Plotly chart (deployed via GitHub Pages)

Output:
    output/
    ├── utah-sb60-income-tax-reduction.md
    └── charts/
        ├── net-income-change.html
        ├── winners-by-decile.html
        └── avg-benefit-by-decile.html

Charts are deployed to GitHub Pages and embedded via iframe in policyengine-app-v2.
"""

# GitHub Pages base URL for chart embeds
GITHUB_PAGES_BASE_URL = "https://policyengine.github.io/utah-sb60-calc"

import os
from utah_sb60 import (
    create_net_income_change_chart,
    create_winners_by_decile_chart,
    create_avg_benefit_by_decile_chart,
    REVENUE_IMPACT_MILLIONS,
    PERCENT_BENEFITING,
    GINI_IMPACT_PCT,
    AVG_BENEFIT_PER_HOUSEHOLD,
    AVG_IMPACT_BY_DECILE,
)

# Create output directories
os.makedirs("output/charts", exist_ok=True)

# Chart HTML template (matching California billionaire tax pattern)
CHART_HTML_TEMPLATE = """<html>
  <head>
    <meta charset="utf-8" />
    <link
      href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap"
      rel="stylesheet"
    />
  </head>
  <body>
    <div>
      <script type="text/javascript">
        window.PlotlyConfig = {{ MathJaxConfig: 'local' }};
      </script>
      <script
        charset="utf-8"
        src="https://cdn.plot.ly/plotly-3.1.1.min.js"
      ></script>
      <div
        id="chart"
        class="plotly-graph-div"
        style="height: 600px; width: 100%"
      ></div>
      <script type="text/javascript">
        window.PLOTLYENV = window.PLOTLYENV || {{}};
        if (document.getElementById('chart')) {{
          Plotly.newPlot(
            'chart',
            {chart_data},
            {chart_layout},
            {{ responsive: true }}
          );
        }}
      </script>
    </div>
  </body>
</html>
"""


def generate_chart_html(fig, filename):
    """Generate a standalone HTML file for a Plotly figure."""
    # Get data and layout from figure
    fig_dict = fig.to_dict()

    # Convert to JSON strings for embedding
    import json
    data_json = json.dumps(fig_dict['data'])
    layout_json = json.dumps(fig_dict['layout'])

    html = CHART_HTML_TEMPLATE.format(
        chart_data=data_json,
        chart_layout=layout_json
    )

    filepath = f"output/charts/{filename}"
    with open(filepath, "w") as f:
        f.write(html)
    print(f"Generated {filepath}")


# Generate chart HTML files
print("Generating chart HTML files...")
generate_chart_html(create_net_income_change_chart(), "net-income-change.html")
generate_chart_html(create_winners_by_decile_chart(), "winners-by-decile.html")
generate_chart_html(create_avg_benefit_by_decile_chart(), "avg-benefit-by-decile.html")

# Generate markdown file
print("Generating markdown file...")

markdown = f"""On January 7th, Senator Daniel McCray (R-Riverton) submitted [SB60](https://le.utah.gov/~2026/bills/static/SB0060.html) to the Utah State Senate. The bill proposes reducing Utah's flat income tax rate from 4.5% to 4.45%, beginning in tax year 2026. This would continue Utah's trend of income tax cuts, marking the fifth consecutive year of rate reductions since the tax rate stood at 4.95% in 2021.

We at PolicyEngine have analyzed the effects of this proposed change on the state of Utah and its residents.

Key results for 2026:

* Reduces state revenues by ${abs(REVENUE_IMPACT_MILLIONS)} million
* Benefits {PERCENT_BENEFITING}% of Utah residents
* Has no effect on the Supplemental Poverty Measure
* Raises the Gini index of inequality by {GINI_IMPACT_PCT}%

*[Use PolicyEngine](https://www.policyengine.org/us) to view the full results or calculate the effect on your household.*

## Tax reform

SB60's proposed 0.05 percentage point reduction would continue the state's pattern of annual income tax cuts. Since 2021, Utah's tax rate has dropped from 4.95% to 4.85% in 2022, 4.65% in 2023, 4.55% in 2024, and 4.5% in 2025.

Unlike the [2025 tax package](https://www.policyengine.org/us/research/utah-income-tax-changes) which included multiple provisions affecting the Child Tax Credit and Social Security credit, SB60 focuses solely on the rate reduction.[^1]

[^1]: SB60 also reduces the state's corporate tax rate to 4.45%. We did not include this provision in our analysis.

## Household impacts

Let's examine how SB60 affects a single adult's net income in Utah. Due to interactions with the Utah taxpayer credit, this household does not benefit with earnings below $20,500. Above this threshold, the taxpayer credit begins to phase out, and tax savings become proportional to earnings. For example, [at $80,000 of earnings](https://app.policyengine.org/us/report-output/sur-mk70207zzf9k), the single adult would see their Utah income tax liability decrease by $40. Figure 1 displays the change in net income for a single adult as earnings rise.

<iframe src="{GITHUB_PAGES_BASE_URL}/net-income-change.html" width="100%" height="650" frameborder="0"></iframe>

## Statewide impacts

For tax year 2026, SB60 would reduce state revenues by ${abs(REVENUE_IMPACT_MILLIONS)} million, according to [PolicyEngine's static modeling](https://app.policyengine.org/us/report-output/sur-mk5j6k3z4m3o).

The tax cut would raise the net income of {PERCENT_BENEFITING}% of residents in Utah. The percentage of residents in each income decile who are net beneficiaries varies, with residents in higher-income deciles more likely to benefit since they have greater taxable income.

<iframe src="{GITHUB_PAGES_BASE_URL}/winners-by-decile.html" width="100%" height="650" frameborder="0"></iframe>

SB60 would provide an average benefit of ${AVG_BENEFIT_PER_HOUSEHOLD} per household, ranging from ${AVG_IMPACT_BY_DECILE[0]} in the bottom income decile to ${AVG_IMPACT_BY_DECILE[-1]} in the top decile.

<iframe src="{GITHUB_PAGES_BASE_URL}/avg-benefit-by-decile.html" width="100%" height="650" frameborder="0"></iframe>

We project that SB60 would have no effect on poverty or deep poverty while raising the state's Gini index of inequality by {GINI_IMPACT_PCT}%.

## Conclusion

SB60 would continue Utah's trend of annual income tax reductions by lowering the flat rate from 4.5% to 4.45% beginning in 2026. The proposal would reduce state revenues while providing tax savings to a majority of Utah taxpayers, with higher-income households receiving larger absolute benefits due to the nature of flat-rate income tax cuts.

As policymakers evaluate reforms such as these, analytical tools like PolicyEngine offer critical insights into the impacts on diverse household compositions and the broader economy.

We invite you to explore our [additional analyses](https://www.policyengine.org/us/research) and use [PolicyEngine](https://www.policyengine.org/us) to calculate your own tax benefits or design custom policy reforms.
"""

with open("output/utah-sb60-income-tax-reduction.md", "w") as f:
    f.write(markdown)
print("Generated output/utah-sb60-income-tax-reduction.md")

print("\n" + "="*60)
print("Done!")
print("="*60)
print("\nCharts will be deployed to GitHub Pages automatically on push.")
print(f"Chart URLs: {GITHUB_PAGES_BASE_URL}/<chart-name>.html")
print("\nTo update policyengine-app-v2, copy the markdown file:")
print("   cp output/utah-sb60-income-tax-reduction.md \\")
print("      ../policyengine-app-v2/app/src/data/posts/articles/")
