import io
import ssl
from math import log1p
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import certifi
import pandas as pd
import plotly.express as px
import streamlit as st
from statsmodels.stats.proportion import (
    confint_proportions_2indep,
    proportions_ztest,
)


# ============================================================
# 1. Configuration
# ============================================================

st.set_page_config(
    page_title="Cookie Cats | A/B Testing Analytics",
    page_icon="🎮",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_PATH = BASE_DIR / "EXPERIMENT_DESIGN.md"

DATA_URL = (
    "https://api.github.com/repos/"
    "KimiyaMirsalehi/cookie-cats-private-data/"
    "contents/cookie_cats.csv"
)

ALPHA = 0.05
CONTROL = "gate_30"
TREATMENT = "gate_40"
GROUP_ORDER = [CONTROL, TREATMENT]

GROUP_LABELS = {
    CONTROL: "Gate 30 (Control)",
    TREATMENT: "Gate 40 (Treatment)",
}

COLORS = {
    "Gate 30 (Control)": "#2563EB",
    "Gate 40 (Treatment)": "#F97316",
}


# ============================================================
# 2. Load data from the private repository
# ============================================================

@st.cache_data(ttl=3600, show_spinner="Loading experiment data...")
def load_data():
    # The token stays on the server and is never displayed.
    token = st.secrets["github"]["token"]
    context = ssl.create_default_context(cafile=certifi.where())

    request = Request(
        DATA_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.raw+json",
            "User-Agent": "cookie-cats-portfolio",
        },
    )

    with urlopen(request, context=context, timeout=30) as response:
        data = pd.read_csv(io.BytesIO(response.read()))

    required_columns = {
        "userid",
        "version",
        "sum_gamerounds",
        "retention_1",
        "retention_7",
    }

    if not required_columns.issubset(data.columns):
        raise ValueError("The dataset is missing required columns.")

    if len(data) != 90189:
        raise ValueError("The dataset does not contain 90,189 rows.")

    if data[list(required_columns)].isna().any().any():
        raise ValueError("The dataset contains missing required values.")

    if not data["userid"].is_unique:
        raise ValueError("The dataset contains duplicate player IDs.")

    if set(data["version"]) != set(GROUP_ORDER):
        raise ValueError("The dataset contains unexpected groups.")

    rounds = pd.to_numeric(data["sum_gamerounds"], errors="raise")

    if (rounds < 0).any() or (rounds % 1 != 0).any():
        raise ValueError("Game rounds must be nonnegative integers.")

    data["sum_gamerounds"] = rounds

    # Normalize CSV boolean values without silently dropping players.
    boolean_mapping = {
        "true": True,
        "false": False,
        "1": True,
        "0": False,
    }

    for column in ["retention_1", "retention_7"]:
        normalized = (
            data[column]
            .astype(str)
            .str.strip()
            .str.lower()
            .map(boolean_mapping)
        )

        if normalized.isna().any():
            raise ValueError("A retention column contains invalid values.")

        data[column] = normalized.astype(bool)

    return data


try:
    df = load_data()
except HTTPError as error:
    if error.code == 401:
        st.error(
            "Dataset authentication failed. "
            "The app owner should check the GitHub token."
        )
    elif error.code in (403, 404):
        st.error(
            "The private dataset could not be accessed. "
            "The app owner should check repository permissions, "
            "the file location, and GitHub API limits."
        )
    else:
        st.error(
            "The dataset service is temporarily unavailable. "
            "Please try again later."
        )
    st.stop()
except (URLError, TimeoutError):
    st.error(
        "Unable to connect to the dataset service. "
        "Please try again later."
    )
    st.stop()
except (FileNotFoundError, KeyError):
    st.error(
        "Dataset credentials are missing. "
        "The app owner should configure the [github] token "
        "in Streamlit secrets."
    )
    st.stop()
except (ValueError, UnicodeError, pd.errors.ParserError):
    st.error(
        "The dataset could not be validated. "
        "The app owner should check the source CSV."
    )
    st.stop()
except Exception:
    # Avoid displaying credentials or detailed connection information.
    st.error(
        "The dataset could not be loaded. "
        "The app owner should check the app configuration."
    )
    st.stop()


# ============================================================
# 3. Header and navigation
# ============================================================

st.title("Cookie Cats | A/B Testing Analytics")
st.write(
    "Explore the experiment comparing the first progression "
    "gate at Level 30 versus Level 40."
)

overview_tab, retention_tab, engagement_tab, report_tab = st.tabs(
    [
        "Overview",
        "Retention & Statistics",
        "Engagement",
        "Final Report",
    ]
)


# ============================================================
# 4. Overview tab
# ============================================================

with overview_tab:
    st.subheader("Experiment Overview")

    st.markdown(
        """
        **Business Question:** Should the developers move
        the first progression gate from Level 30 to Level 40?

        - **Control:** Gate 30
        - **Treatment:** Gate 40
        - **Primary metric:** Day 7 retention
        - **Secondary metrics:** Day 1 retention and game rounds
        """
    )

    st.subheader("Experiment KPIs")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Players", f"{len(df):,}")
    col2.metric(
        "Control Players",
        f"{(df['version'] == CONTROL).sum():,}",
    )
    col3.metric(
        "Treatment Players",
        f"{(df['version'] == TREATMENT).sum():,}",
    )
    col4.metric(
        "Overall Day 7 Retention",
        f"{df['retention_7'].mean() * 100:.2f}%",
    )

    st.info(
        "Use the tabs above to explore retention, statistical "
        "evidence, player engagement, and the experiment design document."
    )

    st.caption(
        "All players are retained in primary analyses. "
        "Outlier exclusion appears only in a separate "
        "engagement sensitivity comparison."
    )

    with st.expander("Statistical assumptions and limitations"):
        st.markdown(
            """
            - Day 7 retention is the primary outcome.
            - Day 1 retention and engagement are secondary metrics.
            - Two-proportion Z-tests assume independent groups.
            - Newcombe confidence intervals describe uncertainty
              in the difference between retention proportions.
            - Displayed confidence intervals are two-sided.
            - Statistical significance does not establish
              commercial significance.
            - Engagement summaries and sensitivity comparisons
              are descriptive; they do not test equivalence.
            - The largest observation is retained in primary
              analyses. Its size alone does not establish an error.
            - The original intended allocation and randomisation
              implementation cannot be independently verified.
            - An earlier sample ratio mismatch (SRM) check produced
              p = 0.008608, above the selected threshold of 0.001
              but below 0.05. This does not prove allocation validity.
            - Any causal interpretation depends on experiment validity.
            """
        )


# ============================================================
# 5. Retention & Statistics tab
# ============================================================

with retention_tab:
    st.subheader("Player Retention Analysis")

    selected_metric = st.selectbox(
        "Select Retention Metric",
        options=["Day 1 Retention", "Day 7 Retention"],
        index=1,
    )

    metric_column = {
        "Day 1 Retention": "retention_1",
        "Day 7 Retention": "retention_7",
    }[selected_metric]

    summary = (
        df.groupby("version")[metric_column]
        .agg(retained="sum", total="count", rate="mean")
        .reindex(GROUP_ORDER)
    )

    control_retained = int(summary.loc[CONTROL, "retained"])
    treatment_retained = int(summary.loc[TREATMENT, "retained"])
    control_total = int(summary.loc[CONTROL, "total"])
    treatment_total = int(summary.loc[TREATMENT, "total"])
    control_rate = float(summary.loc[CONTROL, "rate"])
    treatment_rate = float(summary.loc[TREATMENT, "rate"])
    difference = treatment_rate - control_rate

    chart_data = pd.DataFrame(
        {
            "Experiment Group": [
                GROUP_LABELS[CONTROL],
                GROUP_LABELS[TREATMENT],
            ],
            "Retention Rate (%)": [
                control_rate * 100,
                treatment_rate * 100,
            ],
        }
    ).set_index("Experiment Group")

    st.bar_chart(
        chart_data,
        y="Retention Rate (%)",
        width="stretch",
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Control Retention", f"{control_rate * 100:.2f}%")
    col2.metric("Treatment Retention", f"{treatment_rate * 100:.2f}%")
    col3.metric(
        "Treatment − Control",
        f"{difference * 100:+.3f} pp",
    )

    st.divider()
    st.subheader("Statistical Significance")

    st.write(
        "The supplementary two-sided analysis compares "
        "retention proportions between the experimental groups."
    )

    counts = [treatment_retained, control_retained]
    sample_sizes = [treatment_total, control_total]

    z_statistic, p_value = proportions_ztest(
        count=counts,
        nobs=sample_sizes,
        alternative="two-sided",
    )

    ci_lower, ci_upper = confint_proportions_2indep(
        count1=treatment_retained,
        nobs1=treatment_total,
        count2=control_retained,
        nobs2=control_total,
        compare="diff",
        method="newcomb",
        alpha=ALPHA,
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Z-Statistic", f"{z_statistic:.4f}")
    col2.metric("Two-Sided P-Value", f"{p_value:.6f}")
    col3.metric(
        "Significant at 5%?",
        "Yes" if p_value < ALPHA else "No",
    )

    st.markdown("#### 95% Confidence Interval")
    st.write(
        f"**Observed difference (Gate 40 − Gate 30):** "
        f"{difference * 100:+.3f} percentage points"
    )
    st.write(
        f"**95% confidence interval:** "
        f"[{ci_lower * 100:+.3f}, {ci_upper * 100:+.3f}] "
        "percentage points"
    )

    st.markdown("#### Interpretation")

    if p_value < ALPHA:
        direction = "lower" if difference < 0 else "higher"
        st.info(
            f"{selected_metric} is statistically significantly "
            f"{direction} for Gate 40 in the supplementary "
            "two-sided comparison (p < 0.05). "
            "Causal interpretation depends on experiment validity."
        )
    else:
        st.info(
            f"The difference in {selected_metric} is not "
            "statistically significant at the 5% level. "
            "This does not establish equivalence."
        )

    if metric_column == "retention_7":
        st.markdown("#### Predefined Primary Hypothesis")
        st.write("**H₀:** Gate 40 does not improve Day 7 retention.")
        st.write("**H₁:** Gate 40 improves Day 7 retention.")

        z_primary, p_primary = proportions_ztest(
            count=counts,
            nobs=sample_sizes,
            alternative="larger",
        )

        st.metric(
            "One-Sided Improvement Test — P-Value",
            f"{p_primary:.6f}",
        )

        if p_primary < ALPHA:
            st.info(
                "The primary test provides statistically significant "
                "evidence of higher Day 7 retention for Gate 40, "
                "subject to experiment validity."
            )
        else:
            st.warning(
                "The primary test does not provide statistically "
                "significant evidence that Gate 40 improves "
                "Day 7 retention."
            )

    st.caption(
        "These calculations retain all players. "
        "See Overview for statistical assumptions and the SRM caveat."
    )


# ============================================================
# 6. Engagement tab
# ============================================================

with engagement_tab:
    st.subheader("Player Engagement Analysis")
    st.write(
        "Game rounds measure player activity. These summaries "
        "include every player, including zero-round players "
        "and the largest observation."
    )

    engagement = (
        df.groupby("version")["sum_gamerounds"]
        .agg(
            players="size",
            mean_rounds="mean",
            median_rounds="median",
            max_rounds="max",
            zero_round_players=lambda values: values.eq(0).sum(),
        )
        .reindex(GROUP_ORDER)
    )

    engagement["zero_round_rate"] = (
        engagement["zero_round_players"]
        / engagement["players"]
        * 100
    )

    for column, group in zip(st.columns(2), GROUP_ORDER):
        with column:
            row = engagement.loc[group]
            st.markdown(f"#### {GROUP_LABELS[group]}")

            col1, col2 = st.columns(2)
            col1.metric("Mean Rounds", f"{row['mean_rounds']:.4f}")
            col2.metric("Median Rounds", f"{row['median_rounds']:.0f}")

            col3, col4 = st.columns(2)
            col3.metric("Maximum Rounds", f"{row['max_rounds']:,.0f}")
            col4.metric(
                "Zero-Round Rate",
                f"{row['zero_round_rate']:.2f}%",
            )

            st.caption(
                f"{int(row['zero_round_players']):,} zero-round "
                f"players out of {int(row['players']):,} players."
            )

    st.divider()
    st.markdown("#### Interactive Game-Round Distribution")

    distribution_scale = st.radio(
        "Choose the horizontal scale",
        options=["Logarithmic (1 + rounds)", "Linear"],
        horizontal=True,
    )

    plot_data = df[["version", "sum_gamerounds"]].copy()
    plot_data["Experiment Group"] = (
        plot_data["version"].map(GROUP_LABELS)
    )

    if distribution_scale == "Logarithmic (1 + rounds)":
        plot_data["chart_rounds"] = (
            plot_data["sum_gamerounds"].map(log1p)
        )
        axis_label = "Game rounds (logarithmic spacing; includes zero)"
    else:
        plot_data["chart_rounds"] = plot_data["sum_gamerounds"]
        axis_label = "Game rounds"

    fig = px.histogram(
        plot_data,
        x="chart_rounds",
        color="Experiment Group",
        category_orders={
            "Experiment Group": [
                GROUP_LABELS[CONTROL],
                GROUP_LABELS[TREATMENT],
            ]
        },
        color_discrete_map=COLORS,
        nbins=60,
        histnorm="percent",
        barmode="overlay",
        opacity=0.60,
        labels={"chart_rounds": axis_label},
        title="Game-round distribution by experimental group",
    )

    fig.update_layout(
        yaxis_title="Players within each group (%)",
        legend_title_text="Experiment Group",
        bargap=0.02,
    )

    if distribution_scale == "Logarithmic (1 + rounds)":
        tick_rounds = [
            0, 1, 5, 10, 20, 50, 100, 500, 1000, 10000, 50000
        ]
        fig.update_xaxes(
            tickmode="array",
            tickvals=[log1p(value) for value in tick_rounds],
            ticktext=[f"{value:,}" for value in tick_rounds],
        )

    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        f"All {len(df):,} players are included. Each group's "
        "bars sum to 100%. Hover over bars to inspect percentages."
    )

    if distribution_scale == "Logarithmic (1 + rounds)":
        st.caption(
            "Bins use log(1 + rounds), while tick labels show "
            "original round counts. Equal chart widths represent "
            "unequal ranges of rounds. Zero-round players are included."
        )
    else:
        st.caption(
            "The largest observation stretches the linear scale. "
            "Use the logarithmic view to inspect the long tail."
        )

    st.divider()
    st.markdown("#### Outlier Sensitivity Analysis")

    largest_index = df["sum_gamerounds"].idxmax()
    largest_player = df.loc[largest_index]
    sensitivity_df = df.drop(index=largest_index)

    primary_means = engagement["mean_rounds"]
    sensitivity_means = (
        sensitivity_df.groupby("version")["sum_gamerounds"]
        .mean()
        .reindex(GROUP_ORDER)
    )

    primary_difference = (
        primary_means.loc[TREATMENT] - primary_means.loc[CONTROL]
    )
    sensitivity_difference = (
        sensitivity_means.loc[TREATMENT]
        - sensitivity_means.loc[CONTROL]
    )

    st.write(
        f"The single largest observation is "
        f"**{int(largest_player['sum_gamerounds']):,} rounds** "
        f"in **{GROUP_LABELS[largest_player['version']]}**."
    )

    sensitivity_table = pd.DataFrame(
        {
            "Analysis": [
                "Primary — all players",
                "Sensitivity — exclude single largest observation",
            ],
            "Players": [len(df), len(sensitivity_df)],
            "Gate 30 Mean": [
                primary_means.loc[CONTROL],
                sensitivity_means.loc[CONTROL],
            ],
            "Gate 40 Mean": [
                primary_means.loc[TREATMENT],
                sensitivity_means.loc[TREATMENT],
            ],
            "Difference (Gate 40 − Gate 30)": [
                primary_difference,
                sensitivity_difference,
            ],
        }
    )

    st.dataframe(
        sensitivity_table.style.format(
            {
                "Players": "{:,.0f}",
                "Gate 30 Mean": "{:.4f}",
                "Gate 40 Mean": "{:.4f}",
                "Difference (Gate 40 − Gate 30)": "{:+.4f}",
            }
        ),
        hide_index=True,
        use_container_width=True,
    )

    col1, col2 = st.columns(2)
    col1.metric(
        "Mean Difference — All Players",
        f"{primary_difference:+.4f} rounds",
    )
    col2.metric(
        "Mean Difference — Sensitivity Only",
        f"{sensitivity_difference:+.4f} rounds",
    )

    st.info(
        "The mean comparison is sensitive to the largest observation. "
        "Removing it is a diagnostic check, not evidence that the "
        "observation is invalid. The sensitivity result does not "
        "establish equal engagement or a causal effect."
    )

    st.caption(
        "Retention tests, engagement KPIs, and the distribution "
        "chart retain all players. Only the sensitivity comparison "
        "excludes one observation."
    )


# ============================================================
# 7. Final Report tab
# ============================================================

with report_tab:
    st.subheader("Experiment Design")
    st.caption(
        "This tab displays the project's EXPERIMENT_DESIGN.md document."
    )

    if st.button("Refresh document", key="refresh_report"):
        st.rerun()

    try:
        report_text = REPORT_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        st.warning(
            "EXPERIMENT_DESIGN.md was not found in the project's "
            "top-level folder. It should sit alongside app and data."
        )
    except (OSError, UnicodeError):
        st.error("Unable to read EXPERIMENT_DESIGN.md.")
    else:
        if report_text.strip():
            st.markdown(report_text)
            st.download_button(
                label="Download experiment design",
                data=report_text,
                file_name="EXPERIMENT_DESIGN.md",
                mime="text/markdown",
            )
        else:
            st.info("EXPERIMENT_DESIGN.md is currently empty.")


# ============================================================
# 8. Footer
# ============================================================

st.divider()
st.caption(
    "Cookie Cats A/B Testing Portfolio Project | "
    "Python, pandas, SciPy, statsmodels, DuckDB, Streamlit and Plotly"
)