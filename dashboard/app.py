import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import textwrap
import re


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="RetailIQ | Revenue Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "dashboard_data.parquet"
)

# =========================================================
# GLOBAL SETTINGS
# =========================================================

# =========================================================
# HTML / MARKDOWN RENDERING
# =========================================================

def _clean_markup(content):
    """Normalize custom HTML before passing it to Streamlit Markdown.

    Streamlit's Markdown parser can turn indented HTML fragments separated by
    blank lines into literal code blocks. We therefore remove indentation and
    blank lines from custom markup. This affects presentation markup only; it
    does not change the underlying analytical data.
    """
    cleaned = textwrap.dedent(str(content)).strip()
    lines = [line.strip() for line in cleaned.splitlines() if line.strip()]
    return "\n".join(lines)


def render_html(content):
    st.markdown(_clean_markup(content), unsafe_allow_html=True)


def render_sidebar(content):
    st.sidebar.markdown(_clean_markup(content), unsafe_allow_html=True)



PLOTLY_CONFIG = {
    "displayModeBar": False,
    "responsive": True
}

# RetailIQ green visual system
GREEN = "#35D07F"
GREEN_BRIGHT = "#7EE787"
TEAL = "#18C79A"
MINT = "#B7F7D0"
DEEP_GREEN = "#0E7C55"
RISK = "#FF7A6E"
AMBER = "#F2C14E"
CHART_GRID = "rgba(150, 255, 200, 0.075)"
GREEN_PALETTE = [GREEN, TEAL, GREEN_BRIGHT, DEEP_GREEN, MINT]


# =========================================================
# CUSTOM CSS
# =========================================================

def load_css():

    css_path = (
        Path(__file__).resolve().parent
        / "style.css"
    )

    if css_path.exists():

        with open(
            css_path,
            "r",
            encoding="utf-8"
        ) as file:

            render_html(
                f"<style>{file.read()}</style>"
            )


load_css()


# =========================================================
# DATA LOADING
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_parquet(DATA_PATH)

    return df


df = load_data()

# =========================================================
# GLOBAL CUSTOMER FIRST PURCHASE
# =========================================================

@st.cache_data
def create_customer_history(data):

    customer_sales = data[
        (data["is_sales"]) &
        (data["customer_id"].notna())
    ].copy()

    first_purchase = (
        customer_sales
        .groupby("customer_id")["invoicedate"]
        .min()
        .rename("first_purchase_date")
        .reset_index()
    )

    return first_purchase


customer_history = create_customer_history(df)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def format_currency(value):

    if pd.isna(value):
        return "£0"

    if abs(value) >= 1_000_000:
        return f"£{value / 1_000_000:.2f}M"

    if abs(value) >= 1_000:
        return f"£{value / 1_000:.1f}K"

    return f"£{value:,.0f}"


def format_number(value):

    if pd.isna(value):
        return "0"

    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"

    if abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K"

    return f"{value:,.0f}"


def format_percent(value):

    if pd.isna(value):
        return "0.0%"

    return f"{value:.1f}%"


def style_plot(fig, height=430):

    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter, Arial, sans-serif",
            color="#A9B8AF"
        ),
        title=dict(
            font=dict(
                size=17,
                color="#F4FAF6"
            ),
            x=0,
            xanchor="left"
        ),
        margin=dict(
            l=20,
            r=20,
            t=55,
            b=25
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#A9B8AF"
            )
        ),
        hoverlabel=dict(
            bgcolor="#0C1711",
            font=dict(
                color="#FFFFFF"
            )
        )
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor="rgba(255,255,255,0.08)",
        tickfont=dict(
            color="#7E9186"
        )
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.055)",
        zeroline=False,
        tickfont=dict(
            color="#7E9186"
        )
    )

    return fig


def add_section_header(title, subtitle=None):

    if subtitle:

        render_html(
            f"""
            <div class="section-header">
                <div class="section-title">{title}</div>
                <div class="section-subtitle">{subtitle}</div>
            </div>
            """
        )

    else:

        render_html(
            f"""
            <div class="section-header">
                <div class="section-title">{title}</div>
            </div>
            """
        )


def insight_card(
    label,
    title,
    description,
    tone="blue"
):

    render_html(
        f"""
        <div class="insight-card {tone}">
            <div class="insight-label">{label}</div>
            <div class="insight-title">{title}</div>
            <div class="insight-description">
                {description}
            </div>
        </div>
        """
    )


# =========================================================
# HEADER / BRAND + LANDING HERO
# =========================================================

render_html(
    """
    <div class="topbar">
        <div class="brand-lockup">
            <div class="brand-icon">◈</div>
            <div>
                <div class="brand-name">RETAIL<span>IQ</span></div>
                <div class="brand-sub">REVENUE INTELLIGENCE SYSTEM</div>
            </div>
        </div>

        <div class="topbar-center">
            <span class="topbar-pill active">LIVE ANALYTICS</span>
            <span class="topbar-pill">UCI ONLINE RETAIL II</span>
        </div>

        <div class="topbar-right">
            <span class="live-dot"></span>
            Python · Pandas · Plotly · Streamlit
        </div>
    </div>
    """
)

render_html(
    """
    <div class="hero-shell">
        <div class="hero-grid">
            <div class="hero-copy">
                <div class="hero-overline">
                    <span class="hero-overline-line"></span>
                    EXECUTIVE ANALYTICS PLATFORM
                </div>
                <div class="hero-heading">
                    Turn retail data into
                    <span>business decisions.</span>
                </div>
                <div class="hero-text">
                    Revenue performance, customer value, product risk and
                    growth drivers — designed as one decision system.
                </div>
                <div class="hero-tags">
                    <span>Revenue</span>
                    <span>Customer Intelligence</span>
                    <span>Product Risk</span>
                    <span>Decision Support</span>
                </div>
            </div>

            <div class="hero-visual">
                <div class="orb orb-a"></div>
                <div class="orb orb-b"></div>
                <div class="hero-mini-card hero-mini-main">
                    <div class="mini-label">REVENUE INTELLIGENCE</div>
                    <div class="mini-title">Read the signal.</div>
                    <div class="mini-line"></div>
                    <div class="mini-bars">
                        <i></i><i></i><i></i><i></i><i></i><i></i><i></i>
                    </div>
                </div>
                <div class="hero-mini-card hero-mini-small">
                    <div class="mini-label">DECISION LAYER</div>
                    <div class="mini-number">RFM</div>
                    <div class="mini-caption">Value · Recency · Frequency</div>
                </div>
            </div>
        </div>

        <div class="hero-bottom">
            <div>
                <span class="hero-bottom-label">DATASET</span>
                <strong>1M+ transaction records</strong>
            </div>
            <div>
                <span class="hero-bottom-label">ANALYSIS</span>
                <strong>Revenue · Customer · Product</strong>
            </div>
            <div>
                <span class="hero-bottom-label">OUTPUT</span>
                <strong>Business actions, not just charts</strong>
            </div>
        </div>
    </div>
    """
)

# =========================================================
# SIDEBAR
# =========================================================

render_sidebar(
    """
    <div class="sidebar-brand">
        <span>◈</span> RETAILIQ
    </div>
    """
)

render_sidebar(
    "### Filters"
)

st.sidebar.caption(
    "Explore the business across time, markets and customer value."
)


# =========================================================
# DATE FILTER
# =========================================================

min_date = df["invoicedate"].min().date()
max_date = df["invoicedate"].max().date()

date_range = st.sidebar.date_input(
    "Analysis period",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:

    start_date = pd.Timestamp(
        date_range[0]
    )

    end_date = (
        pd.Timestamp(date_range[1])
        + pd.Timedelta(days=1)
    )

else:

    start_date = pd.Timestamp(min_date)

    end_date = (
        pd.Timestamp(max_date)
        + pd.Timedelta(days=1)
    )


# =========================================================
# COUNTRY FILTER
# =========================================================

countries = sorted(
    df["country"]
    .dropna()
    .unique()
)

selected_countries = st.sidebar.multiselect(
    "Market",
    countries,
    default=[]
)


# =========================================================
# CUSTOMER SEGMENT FILTER
# =========================================================

segments = [
    "Champions",
    "Loyal Customers",
    "Potential Loyalists",
    "At Risk",
    "Lost"
]

selected_segments = st.sidebar.multiselect(
    "Customer segment",
    segments,
    default=[]
)


# =========================================================
# SALES SCOPE
# =========================================================

sales_scope = st.sidebar.radio(
    "Sales scope",
    [
        "All valid sales",
        "Regular products only"
    ],
    index=0
)


# =========================================================
# FILTER SUMMARY
# =========================================================

render_sidebar(
    "---"
)

render_sidebar(
    """
    <div class="sidebar-note">
        <strong>Data note</strong><br>
        December 2011 is a partial month and ends on
        9 December.
    </div>
    """
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df[
    (df["invoicedate"] >= start_date) &
    (df["invoicedate"] < end_date)
].copy()


if selected_countries:

    filtered_df = filtered_df[
        filtered_df["country"].isin(
            selected_countries
        )
    ]


if selected_segments:

    filtered_df = filtered_df[
        filtered_df["customer_segment"].isin(
            selected_segments
        )
    ]


# =========================================================
# VALID SALES
# =========================================================

sales_df = filtered_df[
    filtered_df["is_sales"]
].copy()


if sales_scope == "Regular products only":

    sales_df = sales_df[
        sales_df["is_regular_product"]
    ].copy()


# =========================================================
# CUSTOMER STATUS
# =========================================================

sales_df = sales_df.merge(
    customer_history,
    on="customer_id",
    how="left"
)

sales_df["customer_status"] = np.where(
    sales_df["customer_id"].isna(),
    "Unknown",
    np.where(
        sales_df["invoicedate"].dt.to_period("M")
        ==
        sales_df["first_purchase_date"]
        .dt.to_period("M"),
        "New",
        "Returning"
    )
)


# =========================================================
# EXECUTIVE KPIs
# =========================================================

revenue = sales_df[
    "sales_revenue"
].sum()

orders = sales_df[
    "invoice"
].nunique()

customers = sales_df[
    sales_df["customer_id"].notna()
]["customer_id"].nunique()

aov = (
    revenue / orders
    if orders > 0
    else 0
)


# Champion revenue

champion_df = sales_df[
    sales_df["customer_segment"]
    == "Champions"
]

champion_revenue = (
    champion_df["sales_revenue"].sum()
)

identified_revenue = (
    sales_df[
        sales_df["customer_id"].notna()
    ]["sales_revenue"].sum()
)

champion_share = (
    champion_revenue /
    identified_revenue *
    100
    if identified_revenue > 0
    else 0
)


# Returning revenue

returning_revenue = sales_df[
    sales_df["customer_status"] == "Returning"
]["sales_revenue"].sum()

returning_share = (
    returning_revenue /
    identified_revenue *
    100
    if identified_revenue > 0
    else 0
)


# =========================================================
# KPI ROW
# =========================================================

render_html(
    """
    <div class="section-kicker">
        EXECUTIVE SNAPSHOT
    </div>
    """
)

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)


with kpi1:

    render_html(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">TOTAL REVENUE</div>
            <div class="kpi-value">
                {format_currency(revenue)}
            </div>
            <div class="kpi-foot">
                Valid sales transactions
            </div>
        </div>
        """
    )


with kpi2:

    render_html(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">ORDERS</div>
            <div class="kpi-value">
                {format_number(orders)}
            </div>
            <div class="kpi-foot">
                Unique sales invoices
            </div>
        </div>
        """
    )


with kpi3:

    render_html(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">CUSTOMERS</div>
            <div class="kpi-value">
                {format_number(customers)}
            </div>
            <div class="kpi-foot">
                Identifiable customers
            </div>
        </div>
        """
    )


with kpi4:

    render_html(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">AVERAGE ORDER VALUE</div>
            <div class="kpi-value">
                {format_currency(aov)}
            </div>
            <div class="kpi-foot">
                Revenue per order
            </div>
        </div>
        """
    )


with kpi5:

    render_html(
        f"""
        <div class="kpi-card accent">
            <div class="kpi-label">CHAMPION REVENUE</div>
            <div class="kpi-value">
                {format_percent(champion_share)}
            </div>
            <div class="kpi-foot">
                Share of identified revenue
            </div>
        </div>
        """
    )


# =========================================================
# NAVIGATION
# =========================================================

render_html(
    "<div class='nav-space'></div>"
)

page = st.radio(
    "Dashboard section",
    [
        "Executive Overview",
        "Customer Intelligence",
        "Product & Revenue Risk"
    ],
    horizontal=True,
    label_visibility="collapsed"
)


# =========================================================
# =========================================================
# EXECUTIVE OVERVIEW
# =========================================================
# =========================================================

if page == "Executive Overview":

    add_section_header(
        "Executive Overview",
        "Revenue performance, growth drivers and customer economics."
    )


    # =====================================================
    # MONTHLY REVENUE
    # =====================================================

    monthly = (
        sales_df
        .assign(
            year_month=sales_df[
                "invoicedate"
            ].dt.to_period("M").astype(str)
        )
        .groupby("year_month")
        .agg(
            revenue=("sales_revenue", "sum"),
            orders=("invoice", "nunique"),
            customers=(
                "customer_id",
                "nunique"
            )
        )
        .reset_index()
    )

    monthly["aov"] = (
        monthly["revenue"] /
        monthly["orders"]
    )

    monthly["revenue_growth"] = (
        monthly["revenue"]
        .pct_change() * 100
    )

    monthly["order_growth"] = (
        monthly["orders"]
        .pct_change() * 100
    )

    monthly["customer_growth"] = (
        monthly["customers"]
        .pct_change() * 100
    )


    # =====================================================
    # REVENUE TREND
    # =====================================================

    col1, col2 = st.columns(
        [2.1, 1]
    )

    with col1:

        fig = px.area(
            monthly,
            x="year_month",
            y="revenue",
            markers=True
        )

        fig.update_traces(
            line=dict(
                color="#35D07F",
                width=3
            ),
            fillcolor="rgba(53,208,127,0.14)",
            marker=dict(
                size=7,
                color="#35D07F"
            )
        )

        fig.update_layout(
            title="Monthly Revenue Performance",
            xaxis_title="",
            yaxis_title="Revenue (£)",
            hovermode="x unified"
        )

        fig = style_plot(
            fig,
            height=430
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config=PLOTLY_CONFIG
        )


    with col2:

        render_html(
            """
            <div class="panel-title">
                Latest business signal
            </div>
            """
        )

        if not monthly.empty:

            latest = monthly.iloc[-1]

            render_html(
                f"""
                <div class="signal-panel">

                    <div class="signal-label">
                        LATEST PERIOD
                    </div>

                    <div class="signal-value">
                        {latest["year_month"]}
                    </div>

                    <div class="signal-row">
                        <span>Revenue</span>
                        <strong>
                            {format_currency(latest["revenue"])}
                        </strong>
                    </div>

                    <div class="signal-row">
                        <span>Orders</span>
                        <strong>
                            {format_number(latest["orders"])}
                        </strong>
                    </div>

                    <div class="signal-row">
                        <span>AOV</span>
                        <strong>
                            {format_currency(latest["aov"])}
                        </strong>
                    </div>

                </div>
                """
            )

            if latest["year_month"] == "2011-12":

                render_html(
                    """
                    <div class="warning-box">
                        <strong>Partial period</strong><br>
                        December 2011 contains data only through
                        9 December. Treat its decline as incomplete
                        rather than a full-month performance signal.
                    </div>
                    """
                )


    # =====================================================
    # GROWTH DRIVER ANALYSIS
    # =====================================================

    add_section_header(
        "Growth Driver Analysis",
        "Revenue can move because of order volume, customer volume or basket value."
    )

    col1, col2 = st.columns(2)

    with col1:

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=monthly["year_month"],
                y=monthly["orders"],
                name="Orders",
                marker_color="#35D07F"
            )
        )

        fig.add_trace(
            go.Scatter(
                x=monthly["year_month"],
                y=monthly["aov"],
                name="AOV",
                mode="lines+markers",
                yaxis="y2",
                line=dict(
                    color="#18C79A",
                    width=3
                )
            )
        )

        fig.update_layout(
            title="Order Volume vs AOV",
            yaxis=dict(
                title="Orders"
            ),
            yaxis2=dict(
                title="AOV (£)",
                overlaying="y",
                side="right"
            ),
            hovermode="x unified"
        )

        fig = style_plot(
            fig,
            height=400
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config=PLOTLY_CONFIG
        )


    with col2:

        # December 2011 is a partial month in the source data.
        # Use the latest complete month for the growth-driver cards so
        # the dashboard does not present an incomplete-month decline
        # as a full-month business deterioration.
        growth_monthly = monthly.copy()

        if not growth_monthly.empty and growth_monthly.iloc[-1]["year_month"] == "2011-12":
            growth_monthly = growth_monthly.iloc[:-1].copy()

        if len(growth_monthly) >= 2:

            latest_growth = growth_monthly.iloc[-1]
            comparison = growth_monthly.iloc[-2]

            revenue_growth = (
                (latest_growth["revenue"] / comparison["revenue"]) - 1
            ) * 100

            order_growth = (
                (latest_growth["orders"] / comparison["orders"]) - 1
            ) * 100

            customer_growth = (
                (latest_growth["customers"] / comparison["customers"]) - 1
            ) * 100

            aov_growth = (
                (latest_growth["aov"] / comparison["aov"]) - 1
            ) * 100

            growth_period_label = latest_growth["year_month"]

        else:

            revenue_growth = 0
            order_growth = 0
            customer_growth = 0
            aov_growth = 0
            growth_period_label = "N/A"


        render_html(
            f"""
            <div class="driver-grid">
                <div class="driver-card">
                    <div class="driver-label">REVENUE GROWTH</div>
                    <div class="driver-value">{revenue_growth:+.1f}%</div>
                </div>

                <div class="driver-card">
                    <div class="driver-label">ORDER GROWTH</div>
                    <div class="driver-value cyan">{order_growth:+.1f}%</div>
                </div>

                <div class="driver-card">
                    <div class="driver-label">CUSTOMER GROWTH</div>
                    <div class="driver-value">{customer_growth:+.1f}%</div>
                </div>

                <div class="driver-card">
                    <div class="driver-label">AOV CHANGE</div>
                    <div class="driver-value amber">{aov_growth:+.1f}%</div>
                </div>
            </div>
            """
        )



    # =====================================================
    # NEW VS RETURNING
    # =====================================================

    add_section_header(
        "New vs Returning Revenue",
        "Understand whether growth is being generated by acquisition or repeat purchasing."
    )

    monthly_customer_mix = (
        sales_df[
            sales_df["customer_status"].isin(
                ["New", "Returning"]
            )
        ]
        .assign(
            year_month=lambda x:
                x["invoicedate"]
                .dt.to_period("M")
                .astype(str)
        )
        .groupby(
            [
                "year_month",
                "customer_status"
            ]
        )
        .agg(
            revenue=("sales_revenue", "sum")
        )
        .reset_index()
    )

    if not monthly_customer_mix.empty:

        fig = px.bar(
            monthly_customer_mix,
            x="year_month",
            y="revenue",
            color="customer_status",
            barmode="stack",
            color_discrete_map={
                "New": "#7EE787",
                "Returning": "#18C79A"
            }
        )

        fig.update_layout(
            title="New vs Returning Customer Revenue",
            xaxis_title="",
            yaxis_title="Revenue (£)",
            hovermode="x unified"
        )

        fig = style_plot(
            fig,
            height=420
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config=PLOTLY_CONFIG
        )


    # =====================================================
    # GEOGRAPHIC PERFORMANCE
    # =====================================================

    add_section_header(
        "Geographic Performance",
        "Revenue concentration across customer markets."
    )

    country_df = (
        sales_df
        .groupby("country")
        .agg(
            revenue=("sales_revenue", "sum"),
            orders=("invoice", "nunique"),
            customers=("customer_id", "nunique")
        )
        .reset_index()
    )

    country_df["aov"] = (
        country_df["revenue"] /
        country_df["orders"]
    )

    country_df = (
        country_df
        .sort_values(
            "revenue",
            ascending=False
        )
        .head(12)
    )

    fig = px.bar(
        country_df.sort_values(
            "revenue"
        ),
        x="revenue",
        y="country",
        orientation="h",
        text_auto=".2s"
    )

    fig.update_traces(
        marker_color="#35D07F"
    )

    fig.update_layout(
        title="Top Markets by Revenue",
        xaxis_title="Revenue (£)",
        yaxis_title=""
    )

    fig = style_plot(
        fig,
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config=PLOTLY_CONFIG
    )


    # =====================================================
    # EXECUTIVE INSIGHTS
    # =====================================================

    add_section_header(
        "Executive Signals"
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        insight_card(
            "CUSTOMER VALUE",
            f"{champion_share:.1f}% of identified revenue",
            "Champions represent a concentrated revenue pool. Retention monitoring should prioritize value, not just customer count.",
            "blue"
        )


    with c2:

        insight_card(
            "REPEAT ECONOMICS",
            f"{returning_share:.1f}% returning revenue",
            "Returning customers contribute the majority of identified customer revenue in the selected scope.",
            "cyan"
        )


    with c3:

        insight_card(
            "DECISION SIGNAL",
            "Volume vs basket value",
            "Late-period growth should be decomposed into orders, customers and AOV before deciding where to invest.",
            "amber"
        )


# =========================================================
# CUSTOMER INTELLIGENCE
# =========================================================

elif page == "Customer Intelligence":

    add_section_header(
        "Customer Intelligence",
        "RFM segmentation, customer concentration and retention economics."
    )


    customer_sales = sales_df[
        sales_df["customer_id"].notna()
    ].copy()


    # =====================================================
    # SEGMENT ECONOMICS
    # =====================================================

    segment_df = (
        customer_sales
        .groupby("customer_segment")
        .agg(
            customers=(
                "customer_id",
                "nunique"
            ),
            revenue=(
                "sales_revenue",
                "sum"
            ),
            orders=(
                "invoice",
                "nunique"
            )
        )
        .reset_index()
    )

    segment_df["revenue_share"] = (
        segment_df["revenue"] /
        segment_df["revenue"].sum() *
        100
    )

    segment_order = [
        "Champions",
        "Loyal Customers",
        "Potential Loyalists",
        "At Risk",
        "Lost"
    ]

    segment_df["customer_segment"] = pd.Categorical(
        segment_df["customer_segment"],
        categories=segment_order,
        ordered=True
    )

    segment_df = segment_df.sort_values(
        "customer_segment"
    )


    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            segment_df,
            x="customer_segment",
            y="revenue",
            text_auto=".2s",
            color="customer_segment",
            color_discrete_sequence=GREEN_PALETTE
        )

        fig.update_traces(
            marker_color="#35D07F"
        )

        fig.update_layout(
            title="Revenue by Customer Segment",
            xaxis_title="",
            yaxis_title="Revenue (£)"
        )

        fig = style_plot(
            fig,
            height=430
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config=PLOTLY_CONFIG
        )


    with col2:

        fig = px.pie(
            segment_df,
            names="customer_segment",
            values="revenue",
            hole=0.62,
            color="customer_segment",
            color_discrete_sequence=GREEN_PALETTE
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent"
        )

        fig.update_layout(
            title="Revenue Share by Segment"
        )

        fig = style_plot(
            fig,
            height=430
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config=PLOTLY_CONFIG
        )


    # =====================================================
    # SEGMENT TABLE
    # =====================================================

    add_section_header(
        "Segment Economics"
    )

    display_segment = segment_df.copy()

    display_segment["revenue"] = (
        display_segment["revenue"]
        .map(format_currency)
    )

    display_segment["revenue_share"] = (
        display_segment["revenue_share"]
        .map(format_percent)
    )

    display_segment.columns = [
        "Customer Segment",
        "Customers",
        "Revenue",
        "Orders",
        "Revenue Share"
    ]

    st.dataframe(
        display_segment,
        use_container_width=True,
        hide_index=True
    )


    # =====================================================
    # CUSTOMER PARETO
    # =====================================================

    add_section_header(
        "Customer Revenue Concentration",
        "How much of the revenue base is generated by the highest-value customers?"
    )

    customer_revenue = (
        customer_sales
        .groupby("customer_id")[
            "sales_revenue"
        ]
        .sum()
        .sort_values(
            ascending=False
        )
        .reset_index()
    )

    if not customer_revenue.empty:

        customer_revenue[
            "cumulative_revenue"
        ] = customer_revenue[
            "sales_revenue"
        ].cumsum()

        customer_revenue[
            "cumulative_share"
        ] = (
            customer_revenue[
                "cumulative_revenue"
            ]
            /
            customer_revenue[
                "sales_revenue"
            ].sum()
            * 100
        )

        customer_revenue[
            "customer_percent"
        ] = (
            np.arange(
                1,
                len(customer_revenue) + 1
            )
            /
            len(customer_revenue)
            * 100
        )

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=customer_revenue[
                    "customer_percent"
                ],
                y=customer_revenue[
                    "cumulative_share"
                ],
                mode="lines",
                line=dict(
                    color="#35D07F",
                    width=3
                ),
                name="Cumulative Revenue"
            )
        )

        fig.add_hline(
            y=80,
            line_dash="dash",
            line_color="#18C79A",
            annotation_text="80% revenue"
        )

        fig.update_layout(
            title="Customer Revenue Pareto",
            xaxis_title="% of Customers",
            yaxis_title="Cumulative Revenue (%)"
        )

        fig = style_plot(
            fig,
            height=430
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config=PLOTLY_CONFIG
        )


    # =====================================================
    # CUSTOMER INSIGHTS
    # =====================================================

    c1, c2, c3 = st.columns(3)

    with c1:

        insight_card(
            "CHAMPIONS",
            f"{champion_share:.1f}% revenue share",
            "A concentrated high-value customer base makes retention monitoring an important business control.",
            "blue"
        )


    with c2:

        at_risk_customers = customer_sales[
            customer_sales[
                "customer_segment"
            ].isin(
                ["At Risk", "Lost"]
            )
        ]["customer_id"].nunique()

        insight_card(
            "RETENTION WATCH",
            f"{format_number(at_risk_customers)} customers",
            "At Risk and Lost segments should be evaluated using historical value and recency rather than treated as one uniform recovery pool.",
            "amber"
        )


    with c3:

        insight_card(
            "BUSINESS QUESTION",
            "Who is driving revenue?",
            "Use RFM and customer concentration together to understand where revenue exposure is concentrated.",
            "cyan"
        )


# =========================================================
# PRODUCT & REVENUE RISK
# =========================================================

elif page == "Product & Revenue Risk":

    add_section_header(
        "Product & Revenue Risk",
        "Regular-product performance, return exposure and transaction anomalies."
    )


    # =====================================================
    # PRODUCT SALES
    # =====================================================

    product_sales = sales_df[
        sales_df["is_regular_product"]
    ].copy()


    # =====================================================
    # TOP PRODUCTS
    # =====================================================

    top_products = (
        product_sales
        .groupby(
            [
                "stockcode",
                "description"
            ]
        )
        .agg(
            revenue=(
                "sales_revenue",
                "sum"
            ),
            quantity=(
                "quantity",
                "sum"
            ),
            orders=(
                "invoice",
                "nunique"
            )
        )
        .reset_index()
        .sort_values(
            "revenue",
            ascending=False
        )
        .head(15)
    )


    fig = px.bar(
        top_products.sort_values(
            "revenue"
        ),
        x="revenue",
        y="description",
        orientation="h",
        text_auto=".2s"
    )

    fig.update_traces(
        marker_color="#35D07F"
    )

    fig.update_layout(
        title="Top Products by Revenue",
        xaxis_title="Revenue (£)",
        yaxis_title=""
    )

    fig = style_plot(
        fig,
        height=520
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config=PLOTLY_CONFIG
    )


    # =====================================================
    # RETURN ANALYSIS
    # =====================================================

    sales_products = (
        product_sales
        .groupby(
            [
                "stockcode",
                "description"
            ]
        )
        .agg(
            sales_revenue=(
                "sales_revenue",
                "sum"
            ),
            sold_quantity=(
                "quantity",
                "sum"
            ),
            orders=(
                "invoice",
                "nunique"
            )
        )
        .reset_index()
    )


    returns = filtered_df[
        (filtered_df["is_regular_product"]) &
        (filtered_df["is_return"])
    ].copy()


    return_products = (
        returns
        .groupby(
            [
                "stockcode",
                "description"
            ]
        )
        .agg(
            returned_quantity=(
                "quantity",
                lambda x: abs(x.sum())
            ),
            return_value=(
                "return_value",
                lambda x: abs(x.sum())
            )
        )
        .reset_index()
    )


    product_risk = sales_products.merge(
        return_products,
        on=[
            "stockcode",
            "description"
        ],
        how="left"
    )


    product_risk[
        "returned_quantity"
    ] = product_risk[
        "returned_quantity"
    ].fillna(0)


    product_risk[
        "return_value"
    ] = product_risk[
        "return_value"
    ].fillna(0)


    product_risk["return_rate"] = (
        product_risk[
            "returned_quantity"
        ]
        /
        product_risk[
            "sold_quantity"
        ].replace(
            0,
            np.nan
        )
        * 100
    )


    product_risk[
        "return_value_rate"
    ] = (
        product_risk[
            "return_value"
        ]
        /
        product_risk[
            "sales_revenue"
        ].replace(
            0,
            np.nan
        )
        * 100
    )


    # =====================================================
    # HIGH-VOLUME RETURN RISK
    # =====================================================

    risk_products = product_risk[
        (product_risk["orders"] >= 20) &
        (product_risk["sold_quantity"] >= 100)
    ].copy()

    risk_products = (
        risk_products
        .sort_values(
            "return_rate",
            ascending=False
        )
        .head(15)
    )


    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            risk_products.sort_values(
                "return_rate"
            ),
            x="return_rate",
            y="description",
            orientation="h",
            text_auto=".1f"
        )

        fig.update_traces(
            marker_color=RISK
        )

        fig.update_layout(
            title="High Return-Rate Products",
            xaxis_title="Return Rate (%)",
            yaxis_title=""
        )

        fig = style_plot(
            fig,
            height=520
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config=PLOTLY_CONFIG
        )


    # =====================================================
    # REVENUE LEAKAGE
    # =====================================================

    with col2:

        monthly_risk = (
            product_sales
            .assign(
                year_month=
                product_sales[
                    "invoicedate"
                ]
                .dt.to_period("M")
                .astype(str)
            )
            .groupby("year_month")
            .agg(
                gross_sales=(
                    "sales_revenue",
                    "sum"
                )
            )
            .reset_index()
        )


        monthly_returns = (
            returns
            .assign(
                year_month=
                returns[
                    "invoicedate"
                ]
                .dt.to_period("M")
                .astype(str)
            )
            .groupby("year_month")
            .agg(
                return_value=(
                    "return_value",
                    lambda x: abs(x.sum())
                )
            )
            .reset_index()
        )


        monthly_risk = monthly_risk.merge(
            monthly_returns,
            on="year_month",
            how="left"
        )


        monthly_risk[
            "return_value"
        ] = monthly_risk[
            "return_value"
        ].fillna(0)


        monthly_risk["net_sales"] = (
            monthly_risk["gross_sales"]
            -
            monthly_risk["return_value"]
        )


        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=monthly_risk["year_month"],
                y=monthly_risk["gross_sales"],
                name="Gross sales",
                mode="lines+markers",
                line=dict(
                    color="#35D07F",
                    width=3
                )
            )
        )

        fig.add_trace(
            go.Scatter(
                x=monthly_risk["year_month"],
                y=monthly_risk["net_sales"],
                name="Net sales after returns",
                mode="lines+markers",
                line=dict(
                    color="#18C79A",
                    width=3
                )
            )
        )

        fig.update_layout(
            title="Revenue Leakage from Returns",
            xaxis_title="",
            yaxis_title="Revenue (£)",
            hovermode="x unified"
        )

        fig = style_plot(
            fig,
            height=520
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config=PLOTLY_CONFIG
        )


    # =====================================================
    # ANOMALY WATCH
    # =====================================================

    add_section_header(
        "Anomaly & Investigation Watch",
        "Records that require business or data-quality investigation before drawing conclusions."
    )


    anomaly_products = product_risk[
        (
            product_risk["return_rate"] >= 100
        ) |
        (
            (
                product_risk["return_rate"] >= 50
            ) &
            (
                product_risk["orders"] <= 5
            )
        )
    ].copy()


    anomaly_products = (
        anomaly_products
        .sort_values(
            [
                "return_rate",
                "sold_quantity"
            ],
            ascending=False
        )
        .head(10)
    )


    if not anomaly_products.empty:

        anomaly_display = anomaly_products[
            [
                "stockcode",
                "description",
                "orders",
                "sold_quantity",
                "returned_quantity",
                "return_rate"
            ]
        ].copy()

        anomaly_display["return_rate"] = (
            anomaly_display["return_rate"]
            .map(
                lambda x:
                f"{x:.1f}%"
            )
        )

        anomaly_display.columns = [
            "Stock Code",
            "Product",
            "Orders",
            "Sold Qty",
            "Returned Qty",
            "Return Rate"
        ]

        st.dataframe(
            anomaly_display,
            use_container_width=True,
            hide_index=True
        )

        render_html(
            """
            <div class="warning-box">
                <strong>Why this matters</strong><br>
                Extremely high return rates can represent genuine
                product problems, bulk reversals or unusual transaction
                records. Investigate the underlying orders before using
                these products as normal performance benchmarks.
            </div>
            """
        )

    else:

        st.success(
            "No major high-return anomalies were detected under the current filters."
        )


    # =====================================================
    # DECISION CENTER
    # =====================================================

    add_section_header(
        "Decision Center",
        "Translate the analysis into concrete business questions and actions."
    )


    d1, d2 = st.columns(2)


    with d1:

        render_html(
            """
            <div class="decision-card">

                <div class="decision-number">
                    01
                </div>

                <div class="decision-title">
                    Protect high-value customers
                </div>

                <div class="decision-evidence">
                    Evidence
                </div>

                <div class="decision-text">
                    Champions account for a highly concentrated
                    share of identified customer revenue.
                </div>

                <div class="decision-action">
                    Action → Monitor recency and purchase-frequency
                    deterioration among high-value customers.
                </div>

            </div>
            """
        )


    with d2:

        render_html(
            """
            <div class="decision-card">

                <div class="decision-number">
                    02
                </div>

                <div class="decision-title">
                    Investigate return exposure
                </div>

                <div class="decision-evidence">
                    Evidence
                </div>

                <div class="decision-text">
                    Several regular products exhibit elevated
                    return behaviour.
                </div>

                <div class="decision-action">
                    Action → Review quality, fulfilment,
                    descriptions and transaction anomalies.
                </div>

            </div>
            """
        )


    d3, d4 = st.columns(2)


    with d3:

        render_html(
            """
            <div class="decision-card">

                <div class="decision-number">
                    03
                </div>

                <div class="decision-title">
                    Improve basket economics
                </div>

                <div class="decision-evidence">
                    Evidence
                </div>

                <div class="decision-text">
                    November growth was strongly volume-driven,
                    with orders increasing while AOV declined.
                </div>

                <div class="decision-action">
                    Action → Investigate product mix,
                    bundles and cross-sell opportunities.
                </div>

            </div>
            """
        )


    with d4:

        render_html(
            """
            <div class="decision-card">

                <div class="decision-number">
                    04
                </div>

                <div class="decision-title">
                    Validate international signals
                </div>

                <div class="decision-evidence">
                    Evidence
                </div>

                <div class="decision-text">
                    Some international markets show high AOV
                    but relatively small customer populations.
                </div>

                <div class="decision-action">
                    Action → Validate repeatability before
                    making broader market-investment decisions.
                </div>

            </div>
            """
        )


# =========================================================
# FOOTER
# =========================================================

render_html(
    """
    <div class="footer">

        <div class="footer-brand">
            ◈ RETAILIQ
        </div>

        <div class="footer-text">
            Revenue & Customer Intelligence
            · Python · Pandas · Plotly · Streamlit
        </div>

        <div class="footer-status">
            Analytical dataset · UCI Online Retail II
        </div>

    </div>
    """
)
