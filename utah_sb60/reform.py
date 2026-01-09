"""Utah SB60 reform definition."""

from policyengine_core.reforms import Reform

# Define the reform: reduce Utah income tax rate from 4.5% to 4.45%
ut_sb60_reform = Reform.from_dict(
    {"gov.states.ut.tax.income.rate": {"2026-01-01.2100-12-31": 0.0445}},
    country_id="us",
)
