"""Chart generation functions for Utah SB60 analysis."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
)

# PolicyEngine app-v2 color palette (teal-based)
BLACK = "#000000"
PRIMARY_TEAL = "#319795"  # colors.primary[500] - main brand color
PRIMARY_TEAL_LIGHT = "#E6FFFA"  # colors.primary[50] - light teal backgrounds
GRAY_600 = "#4B5563"  # Negative/losses
GRAY_300 = "#D1D5DB"  # Neutral/no change
GRAY_400 = "#9CA3AF"  # Secondary gray

# Chart watermark configuration
WATERMARK_CONFIG = {
    "source": "/assets/logos/policyengine/teal-square-transparent.png",
    "xref": "paper",
    "yref": "paper",
    "sizex": 0.07,
    "sizey": 0.07,
    "xanchor": "right",
    "yanchor": "bottom",
}


def create_net_income_change_chart() -> go.Figure:
    """
    Create Figure 1: Change in net income for a single adult.

    Returns:
        Plotly figure object
    """
    employment_income_values, net_income_changes = calculate_net_income_changes()

    df = pd.DataFrame(
        {
            "Employment Income": employment_income_values,
            "Change in net income": net_income_changes,
        }
    )

    fig = px.line(
        df,
        x="Employment Income",
        y="Change in net income",
        color_discrete_sequence=[PRIMARY_TEAL],
        title="Figure 1: Change in net income for a single adult",
    ).update_layout(
        font=dict(family="Roboto Serif"),
        xaxis_title="Employment income ($)",
        yaxis_title="Change in net income ($)",
        xaxis_tickformat=",",
        yaxis_tickformat=",",
        font_color=BLACK,
        margin={"l": 60, "r": 60, "b": 80, "t": 80, "pad": 4},
        images=[
            {
                **WATERMARK_CONFIG,
                "x": 1.05,
                "y": -0.18,
            }
        ],
    ).update_traces(
        hovertemplate="Employment income: $%{x:,}<br>Change in net income: $%{y:.2f}<extra></extra>"
    )

    return fig


def create_winners_by_decile_chart() -> go.Figure:
    """
    Create Figure 2: Winners of Utah SB60 by income decile.

    Returns:
        Plotly figure object
    """
    labels_deciles = [f"{i}" for i in DECILES]

    df_deciles = pd.DataFrame(
        {
            "Income decile": labels_deciles,
            "Gain more than 5%": GAIN_MORE_THAN_5PCT,
            "Gain less than 5%": GAIN_LESS_THAN_5PCT,
            "No change": NO_CHANGE,
            "Loss less than 5%": LOSS_LESS_THAN_5PCT,
            "Loss more than 5%": LOSS_MORE_THAN_5PCT,
        }
    )

    df_all = pd.DataFrame(
        {
            "Income decile": ["All"],
            "Gain more than 5%": [ALL_GAIN_MORE_THAN_5PCT],
            "Gain less than 5%": [ALL_GAIN_LESS_THAN_5PCT],
            "No change": [ALL_NO_CHANGE],
            "Loss less than 5%": [ALL_LOSS_LESS_THAN_5PCT],
            "Loss more than 5%": [ALL_LOSS_MORE_THAN_5PCT],
        }
    )

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
        row_heights=[0.1, 0.9],
    )

    # Colors
    COLOR_GAIN_MORE = PRIMARY_TEAL
    COLOR_GAIN_LESS = PRIMARY_TEAL_LIGHT
    COLOR_NO_CHANGE = GRAY_300
    COLOR_LOSS_LESS = GRAY_400
    COLOR_LOSS_MORE = GRAY_600

    # Add traces for "All" category - first row
    _add_stacked_bar_traces(
        fig, df_all, COLOR_GAIN_MORE, COLOR_GAIN_LESS,
        COLOR_NO_CHANGE, COLOR_LOSS_LESS, COLOR_LOSS_MORE,
        row=1, show_legend=True
    )

    # Add traces for deciles - second row
    _add_stacked_bar_traces(
        fig, df_deciles, COLOR_GAIN_MORE, COLOR_GAIN_LESS,
        COLOR_NO_CHANGE, COLOR_LOSS_LESS, COLOR_LOSS_MORE,
        row=2, show_legend=False
    )

    fig.update_layout(
        barmode="stack",
        title=dict(text="Figure 2: Winners of Utah SB60 by income decile", x=0),
        font=dict(family="Roboto Serif"),
        xaxis=dict(title="", ticksuffix="%", range=[0, 100]),
        xaxis2=dict(
            title=dict(text="Population share", standoff=20),
            ticksuffix="%",
            range=[0, 100],
        ),
        yaxis2=dict(
            title=dict(text="Income decile", standoff=15),
            automargin=True,
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            traceorder="normal",
            font=dict(size=11),
        ),
        font_color=BLACK,
        margin={"l": 60, "r": 60, "b": 80, "t": 100, "pad": 4},
        height=550,
        width=800,
        images=[
            {
                **WATERMARK_CONFIG,
                "x": 1.05,
                "y": -0.16,
            }
        ],
    )

    return fig


def _add_stacked_bar_traces(
    fig: go.Figure,
    df: pd.DataFrame,
    color_gain_more: str,
    color_gain_less: str,
    color_no_change: str,
    color_loss_less: str,
    color_loss_more: str,
    row: int,
    show_legend: bool,
) -> None:
    """Add stacked bar traces to a figure."""
    categories = [
        ("Gain more than 5%", "Gain >5%", color_gain_more, None),
        ("Gain less than 5%", "Gain <5%", color_gain_less, BLACK),
        ("No change", "No change", color_no_change, BLACK),
        ("Loss less than 5%", "Loss <5%", color_loss_less, None),
        ("Loss more than 5%", "Loss >5%", color_loss_more, None),
    ]

    for col_name, legend_name, color, text_color in categories:
        text_kwargs = {}
        if text_color:
            text_kwargs["textfont"] = dict(color=text_color)

        fig.add_trace(
            go.Bar(
                y=df["Income decile"],
                x=df[col_name],
                name=legend_name,
                orientation="h",
                marker_color=color,
                text=[f"{x}%" if x > 0 else "" for x in df[col_name]],
                textposition="inside",
                legendgroup=col_name.lower().replace(" ", "_"),
                showlegend=show_legend,
                hovertemplate="%{x}%<extra></extra>",
                **text_kwargs,
            ),
            row=row,
            col=1,
        )


def create_avg_benefit_by_decile_chart() -> go.Figure:
    """
    Create Figure 3: Average benefit of Utah SB60 by income decile.

    Returns:
        Plotly figure object
    """
    df = pd.DataFrame(
        {
            "Income decile": DECILES,
            "Average impact": AVG_IMPACT_BY_DECILE,
        }
    )

    dollar_text = [f"${x}" for x in AVG_IMPACT_BY_DECILE]

    fig = (
        px.bar(
            df,
            x="Income decile",
            y="Average impact",
            text=dollar_text,
            color_discrete_sequence=[PRIMARY_TEAL],
            title="Figure 3: Average benefit of Utah SB60 by income decile",
        )
        .update_layout(
            font=dict(family="Roboto Serif"),
            xaxis_title="Income decile",
            yaxis_title="Average impact ($)",
            xaxis_tickvals=list(range(1, 11)),
            yaxis_tickformat=",",
            showlegend=False,
            font_color=BLACK,
            margin={"l": 60, "r": 60, "b": 80, "t": 80, "pad": 4},
            images=[
                {
                    **WATERMARK_CONFIG,
                    "x": 1.05,
                    "y": -0.18,
                }
            ],
        )
        .update_traces(
            hovertemplate="Income decile: %{x}<br>Average impact: $%{y:,.0f}<extra></extra>"
        )
    )

    return fig
