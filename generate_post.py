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

# Chart metadata for SEO (title, description per chart)
CHART_SEO_METADATA = {
    "net-income-change.html": {
        "title": "Utah SB60: Change in Net Income for a Single Adult | PolicyEngine",
        "description": (
            "Interactive chart showing how Utah SB60's income tax rate reduction "
            "from 4.5% to 4.45% affects net income for a single adult across "
            "different earnings levels."
        ),
        "chart_label": (
            "Line chart showing the change in net income for a single adult "
            "under Utah SB60 across employment income levels from $0 to $200,000"
        ),
    },
    "winners-by-decile.html": {
        "title": "Utah SB60: Winners by Income Decile | PolicyEngine",
        "description": (
            "Interactive chart showing the share of Utah residents who benefit "
            "from SB60's income tax reduction, broken down by income decile."
        ),
        "chart_label": (
            "Stacked bar chart showing the percentage of Utah residents in each "
            "income decile who gain or lose from SB60"
        ),
    },
    "avg-benefit-by-decile.html": {
        "title": "Utah SB60: Average Benefit by Income Decile | PolicyEngine",
        "description": (
            "Interactive chart showing the average household benefit from "
            "Utah SB60's income tax reduction by income decile, ranging from "
            "$5 to $583."
        ),
        "chart_label": (
            "Bar chart showing the average household income change under Utah "
            "SB60 for each income decile"
        ),
    },
}

# Chart HTML template with SEO improvements
CHART_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{chart_title}</title>
    <meta name="description" content="{chart_description}" />
    <meta name="robots" content="index, follow" />
    <link rel="canonical" href="{chart_canonical_url}" />

    <!-- Open Graph -->
    <meta property="og:type" content="article" />
    <meta property="og:title" content="{chart_title}" />
    <meta property="og:description" content="{chart_description}" />
    <meta property="og:url" content="{chart_canonical_url}" />
    <meta property="og:site_name" content="PolicyEngine" />
    <meta property="og:image" content="{base_url}/assets/teal-square.png" />

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary" />
    <meta name="twitter:title" content="{chart_title}" />
    <meta name="twitter:description" content="{chart_description}" />
    <meta name="twitter:image" content="{base_url}/assets/teal-square.png" />

    <!-- Structured Data (JSON-LD) -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Dataset",
      "name": "{chart_title}",
      "description": "{chart_description}",
      "url": "{chart_canonical_url}",
      "creator": {{
        "@type": "Organization",
        "name": "PolicyEngine",
        "url": "https://policyengine.org"
      }},
      "license": "https://opensource.org/licenses/MIT",
      "isPartOf": {{
        "@type": "WebSite",
        "name": "PolicyEngine",
        "url": "https://policyengine.org"
      }}
    }}
    </script>

    <!-- Preconnect for performance -->
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link rel="preconnect" href="https://cdn.plot.ly" />
    <link
      href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap"
      rel="stylesheet"
    />
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-2YHG89FY0N"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-2YHG89FY0N', {{ tool_name: 'utah-sb60-calc' }});
    </script>
    <script>
    (function() {{
      var TOOL_NAME = 'utah-sb60-calc';
      if (typeof window === 'undefined' || !window.gtag) return;

      var scrollFired = {{}};
      window.addEventListener('scroll', function() {{
        var docHeight = document.documentElement.scrollHeight - window.innerHeight;
        if (docHeight <= 0) return;
        var pct = Math.floor((window.scrollY / docHeight) * 100);
        [25, 50, 75, 100].forEach(function(m) {{
          if (pct >= m && !scrollFired[m]) {{
            scrollFired[m] = true;
            window.gtag('event', 'scroll_depth', {{ percent: m, tool_name: TOOL_NAME }});
          }}
        }});
      }}, {{ passive: true }});

      [30, 60, 120, 300].forEach(function(sec) {{
        setTimeout(function() {{
          if (document.visibilityState !== 'hidden') {{
            window.gtag('event', 'time_on_tool', {{ seconds: sec, tool_name: TOOL_NAME }});
          }}
        }}, sec * 1000);
      }});

      document.addEventListener('click', function(e) {{
        var link = e.target && e.target.closest ? e.target.closest('a') : null;
        if (!link || !link.href) return;
        try {{
          var url = new URL(link.href, window.location.origin);
          if (url.hostname && url.hostname !== window.location.hostname) {{
            window.gtag('event', 'outbound_click', {{
              url: link.href,
              target_hostname: url.hostname,
              tool_name: TOOL_NAME
            }});
          }}
        }} catch (err) {{}}
      }});
    }})();
    </script>
  </head>
  <body>
    <main>
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
        role="img"
        aria-label="{chart_aria_label}"
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
    </main>
  </body>
</html>
"""


def generate_chart_html(fig, filename):
    """Generate a standalone HTML file for a Plotly figure."""
    import json
    import plotly.io as pio

    # Use Plotly's JSON serialization which handles numpy arrays
    fig_json = json.loads(pio.to_json(fig))
    data_json = json.dumps(fig_json['data'])
    layout_json = json.dumps(fig_json['layout'])

    # Get SEO metadata for this chart
    seo = CHART_SEO_METADATA.get(filename, {})
    chart_title = seo.get("title", f"Utah SB60 Chart | PolicyEngine")
    chart_description = seo.get("description", "Utah SB60 income tax analysis chart by PolicyEngine.")
    chart_aria_label = seo.get("chart_label", "Interactive chart from PolicyEngine Utah SB60 analysis")
    chart_canonical_url = f"{GITHUB_PAGES_BASE_URL}/{filename}"

    html = CHART_HTML_TEMPLATE.format(
        chart_data=data_json,
        chart_layout=layout_json,
        chart_title=chart_title,
        chart_description=chart_description,
        chart_aria_label=chart_aria_label,
        chart_canonical_url=chart_canonical_url,
        base_url=GITHUB_PAGES_BASE_URL,
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

<iframe src="{GITHUB_PAGES_BASE_URL}/net-income-change.html" title="Figure 1: Change in net income for a single adult under Utah SB60" width="100%" height="650" frameborder="0"></iframe>

## Statewide impacts

For tax year 2026, SB60 would reduce state revenues by ${abs(REVENUE_IMPACT_MILLIONS)} million, according to [PolicyEngine's static modeling](https://app.policyengine.org/us/report-output/sur-mk5j6k3z4m3o).

The tax cut would raise the net income of {PERCENT_BENEFITING}% of residents in Utah. The percentage of residents in each income decile who are net beneficiaries varies, with residents in higher-income deciles more likely to benefit since they have greater taxable income.

<iframe src="{GITHUB_PAGES_BASE_URL}/winners-by-decile.html" title="Figure 2: Winners of Utah SB60 by income decile" width="100%" height="650" frameborder="0"></iframe>

SB60 would provide an average benefit of ${AVG_BENEFIT_PER_HOUSEHOLD} per household, ranging from ${AVG_IMPACT_BY_DECILE[0]} in the bottom income decile to ${AVG_IMPACT_BY_DECILE[-1]} in the top decile.

<iframe src="{GITHUB_PAGES_BASE_URL}/avg-benefit-by-decile.html" title="Figure 3: Average benefit of Utah SB60 by income decile" width="100%" height="650" frameborder="0"></iframe>

We project that SB60 would have no effect on poverty or deep poverty while raising the state's Gini index of inequality by {GINI_IMPACT_PCT}%.

## Conclusion

SB60 would continue Utah's trend of annual income tax reductions by lowering the flat rate from 4.5% to 4.45% beginning in 2026. The proposal would reduce state revenues while providing tax savings to a majority of Utah taxpayers, with higher-income households receiving larger absolute benefits due to the nature of flat-rate income tax cuts.

As policymakers evaluate reforms such as these, analytical tools like PolicyEngine offer critical insights into the impacts on diverse household compositions and the broader economy.

We invite you to explore our [additional analyses](https://www.policyengine.org/us/research) and use [PolicyEngine](https://www.policyengine.org/us) to calculate your own tax benefits or design custom policy reforms.
"""

with open("output/utah-sb60-income-tax-reduction.md", "w") as f:
    f.write(markdown)
print("Generated output/utah-sb60-income-tax-reduction.md")

# Generate robots.txt for GitHub Pages
print("Generating robots.txt...")
robots_txt = f"""User-agent: *
Allow: /

Sitemap: {GITHUB_PAGES_BASE_URL}/sitemap.xml
"""
with open("output/robots.txt", "w") as f:
    f.write(robots_txt)
print("Generated output/robots.txt")

# Generate sitemap.xml for GitHub Pages
print("Generating sitemap.xml...")
chart_filenames = ["net-income-change.html", "winners-by-decile.html", "avg-benefit-by-decile.html"]
sitemap_urls = "\n".join(
    f"""  <url>
    <loc>{GITHUB_PAGES_BASE_URL}/{name}</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>"""
    for name in chart_filenames
)
sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{sitemap_urls}
</urlset>
"""
with open("output/sitemap.xml", "w") as f:
    f.write(sitemap_xml)
print("Generated output/sitemap.xml")

print("\n" + "="*60)
print("Done!")
print("="*60)
print("\nCharts will be deployed to GitHub Pages automatically on push.")
print(f"Chart URLs: {GITHUB_PAGES_BASE_URL}/<chart-name>.html")
print("\nTo update policyengine-app-v2, copy the markdown file:")
print("   cp output/utah-sb60-income-tax-reduction.md \\")
print("      ../policyengine-app-v2/app/src/data/posts/articles/")
