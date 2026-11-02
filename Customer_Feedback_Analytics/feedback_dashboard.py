
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Customer Feedback Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Customer Feedback Analytics Dashboard")
st.caption(
    "Analyze customer ratings, sentiment, review trends, "
    "and geographical feedback."
)

# ============================================================
# 2. DATA SOURCE
# ============================================================

CSV_PATH = Path(
    r"E:\data_analytics\mongoDB\customer_feedback_cleaned.csv"
)


# ============================================================
# 3. LOAD AND PREPARE DATA
# ============================================================

@st.cache_data(ttl=300)
def load_data(file_path):
    df = pd.read_csv(file_path, low_memory=False)

    # Remove unnecessary spaces from column names
    df.columns = df.columns.str.strip()

    # Check required columns
    required_columns = ["stars_review", "rating_review"]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Clean sentiment labels
    df["rating_review"] = (
        df["rating_review"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    # Convert review ratings to numeric
    df["stars_review"] = pd.to_numeric(
        df["stars_review"],
        errors="coerce"
    )

    # Convert date column to datetime when available
    if "date" in df.columns:
       df["date"] = pd.to_datetime(
    df["date"],
    format="%d/%m/%Y %H:%M",
    errors="coerce"
)
    
        

    # Clean location columns
    for col in ["state", "city", "categories", "name", "text"]:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype("string")
                .str.strip()
            )

    return df


# ============================================================
# 4. READ DATA SAFELY
# ============================================================

if not CSV_PATH.exists():
    st.error(f"CSV file not found: {CSV_PATH}")
    st.info(
        "Check the file location and ensure the filename "
        "is customer_feedback_cleaned.csv."
    )
    st.stop()

try:
    df = load_data(str(CSV_PATH))
except Exception as error:
    st.error(f"Unable to load the dataset: {error}")
    st.stop()

if df.empty:
    st.warning("The CSV file contains no records.")
    st.stop()

# Keep only recognised sentiment labels for sentiment visuals
valid_sentiments = ["positive", "negative", "neutral"]

# ============================================================
# 5. SIDEBAR FILTERS
# ============================================================

st.sidebar.header("🔎 Dashboard Filters")

filtered_df = df.copy()

# Date filter
if "date" in df.columns and df["date"].notna().any():
    min_date = df["date"].min().date()
    max_date = df["date"].max().date()

    selected_dates = st.sidebar.date_input(
        "Select review date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    if isinstance(selected_dates, (tuple, list)):
        if len(selected_dates) == 2:
            start_date, end_date = selected_dates

            filtered_df = filtered_df[
                filtered_df["date"].notna()
                & (
                    filtered_df["date"].dt.date
                    >= start_date
                )
                & (
                    filtered_df["date"].dt.date
                    <= end_date
                )
            ]
        elif len(selected_dates) == 1:
            selected_date = selected_dates[0]
            filtered_df = filtered_df[
                filtered_df["date"].dt.date == selected_date
            ]

# State filter
if "state" in df.columns:
    state_values = sorted(
        df["state"].dropna().astype(str).unique().tolist()
    )

    selected_states = st.sidebar.multiselect(
        "Select state",
        options=state_values
    )

    if selected_states:
        filtered_df = filtered_df[
            filtered_df["state"].isin(selected_states)
        ]

# City filter
if "city" in df.columns:
    available_cities = sorted(
        filtered_df["city"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_cities = st.sidebar.multiselect(
        "Select city",
        options=available_cities
    )

    if selected_cities:
        filtered_df = filtered_df[
            filtered_df["city"].isin(selected_cities)
        ]

# Sentiment filter
sentiment_options = ["positive", "negative", "neutral"]

selected_sentiments = st.sidebar.multiselect(
    "Select sentiment",
    options=sentiment_options,
    default=sentiment_options
)

if selected_sentiments:
    filtered_df = filtered_df[
        filtered_df["rating_review"].isin(selected_sentiments)
    ]
else:
    filtered_df = filtered_df.iloc[0:0]

st.sidebar.divider()
st.sidebar.caption(
    "All dashboard metrics and charts respond to the selected filters."
)

if filtered_df.empty:
    st.warning(
        "No reviews match the selected filters. "
        "Change or clear the filters to see results."
    )
    st.stop()

# ============================================================
# 6. KPI CALCULATIONS
# ============================================================

total_reviews = len(filtered_df)

average_rating = filtered_df["stars_review"].mean()

sentiment_series = (
    filtered_df["rating_review"]
    .astype("string")
    .str.strip()
    .str.lower()
)

positive_count = int(
    sentiment_series.eq("positive").sum()
)

negative_count = int(
    sentiment_series.eq("negative").sum()
)

neutral_count = int(
    sentiment_series.eq("neutral").sum()
)

labelled_reviews = int(
    sentiment_series.isin(valid_sentiments).sum()
)

positive_percentage = (
    positive_count / total_reviews * 100
    if total_reviews > 0 else 0
)

negative_percentage = (
    negative_count / total_reviews * 100
    if total_reviews > 0 else 0
)

neutral_percentage = (
    neutral_count / total_reviews * 100
    if total_reviews > 0 else 0
)



# ============================================================
# 7. KPI CARDS
# ============================================================

# ---------------- KPI DISPLAY ----------------

st.subheader("📌 Key Performance Indicators")

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

# Total Reviews
with kpi1:
    st.markdown(
        f"""
        <div style="text-align:center;">
            <p style="font-size:15px; margin:0;">Total Reviews</p>
            <h2 style="margin:5px 0 0 0;">{total_reviews:,}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

# Average Rating
with kpi2:
    st.markdown(
        f"""
        <div style="text-align:center;">
            <p style="font-size:15px; margin:0;">Average Rating</p>
            <h2 style="margin:5px 0 0 0;">{average_rating:.2f} / 5</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

# Positive Sentiment
with kpi3:
    st.markdown(
        f"""
        <div style="text-align:center;">
            <p style="font-size:15px; margin:0;">Positive</p>
            <h2 style="color:#21C55D; margin:5px 0 0 0;">
                {positive_percentage:.2f}%
            </h2>
            <p style="font-size:12px; color:gray; margin:0;">
                {positive_count:,} reviews
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Negative Sentiment
with kpi4:
    st.markdown(
        f"""
        <div style="text-align:center;">
            <p style="font-size:15px; margin:0;">Negative</p>
            <h2 style="color:#EF4444; margin:5px 0 0 0;">
                {negative_percentage:.2f}%
            </h2>
            <p style="font-size:12px; color:gray; margin:0;">
                {negative_count:,} reviews
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Neutral Sentiment
with kpi5:
    st.markdown(
        f"""
        <div style="text-align:center;">
            <p style="font-size:15px; margin:0;">Neutral</p>
            <h2 style="color:#9CA3AF; margin:5px 0 0 0;">
                {neutral_percentage:.2f}%
            </h2>
            <p style="font-size:12px; color:gray; margin:0;">
                {neutral_count:,} reviews
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# 8. DATA QUALITY SUMMARY
# ============================================================

with st.expander("📋 View data quality summary"):
    quality1, quality2, quality3, quality4 = st.columns(4)

    quality1.metric(
        "Rows in CSV",
        f"{len(df):,}"
    )

    quality2.metric(
        "Columns",
        f"{len(df.columns):,}"
    )

    quality3.metric(
        "Missing Ratings",
        f"{df['stars_review'].isna().sum():,}"
    )

    quality4.metric(
        "Missing Sentiment Labels",
        f"{(~df['rating_review'].isin(valid_sentiments)).sum():,}"
    )

    st.write("Missing values by column:")
    missing_data = (
        df.isna()
        .sum()
        .reset_index()
    )
    missing_data.columns = ["Column", "Missing Values"]
    missing_data = missing_data.sort_values(
        "Missing Values",
        ascending=False
    )

    st.dataframe(
        missing_data,
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# 9. REVIEW RATING ANALYSIS
# ============================================================

st.header("⭐ Review Rating Analysis")

rating_df = filtered_df.dropna(
    subset=["stars_review"]
).copy()

if not rating_df.empty:
    rating_counts = (
        rating_df["stars_review"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    rating_counts.columns = ["Rating", "Review Count"]

    col1, col2 = st.columns(2)

    with col1:
        fig_rating_bar = px.bar(
            rating_counts,
            x="Rating",
            y="Review Count",
            text="Review Count",
            title="Review Count by Star Rating",
            labels={
                "Rating": "Star Rating",
                "Review Count": "Number of Reviews"
            }
        )

        fig_rating_bar.update_layout(
            xaxis=dict(dtick=1),
            showlegend=False
        )

        st.plotly_chart(
            fig_rating_bar,
            use_container_width=True
        )

    with col2:
        fig_rating_pie = px.pie(
            rating_counts,
            names="Rating",
            values="Review Count",
            title="Share of Reviews by Star Rating",
            hole=0.35
        )

        st.plotly_chart(
            fig_rating_pie,
            use_container_width=True
        )
else:
    st.info("No valid star ratings are available for these filters.")

# ============================================================
# 10. SENTIMENT ANALYSIS USING rating_review
# ============================================================

st.header("💬 Sentiment Analysis")

st.caption(
    "Sentiment visuals use the existing rating_review field "
    "in the cleaned CSV. Labels are normalised to lowercase "
    "for consistent counting."
)

sentiment_counts = (
    sentiment_series[
        sentiment_series.isin(valid_sentiments)
    ]
    .value_counts()
    .reindex(valid_sentiments, fill_value=0)
    .rename_axis("Sentiment")
    .reset_index(name="Review Count")
)

sentiment_counts["Percentage"] = (
    sentiment_counts["Review Count"]
    / labelled_reviews * 100
    if labelled_reviews > 0
    else 0
)

col1, col2 = st.columns(2)

with col1:
    fig_sentiment_bar = px.bar(
        sentiment_counts,
        x="Sentiment",
        y="Review Count",
        text="Review Count",
        title="Number of Reviews by Sentiment",
        category_orders={
            "Sentiment": ["negative", "neutral", "positive"]
        },
        labels={
            "Review Count": "Number of Reviews",
            "Sentiment": "Sentiment"
        }
    )

    st.plotly_chart(
        fig_sentiment_bar,
        use_container_width=True
    )

with col2:
    fig_sentiment_pie = px.pie(
        sentiment_counts,
        names="Sentiment",
        values="Review Count",
        title="Sentiment Distribution (%)",
        hole=0.35
    )

    fig_sentiment_pie.update_traces(
        textinfo="percent+label"
    )

    st.plotly_chart(
        fig_sentiment_pie,
        use_container_width=True
    )

st.subheader("Sentiment Summary")

st.dataframe(
    sentiment_counts.style.format({
        "Percentage": "{:.2f}%"
    }),
    use_container_width=True,
    hide_index=True
)

# ============================================================
# 11. MONTHLY REVIEW TRENDS
# ============================================================

st.header("📅 Monthly Review Trends")

if "date" in filtered_df.columns:
    monthly_df = filtered_df.dropna(
        subset=["date"]
    ).copy()

    if not monthly_df.empty:
        monthly_df["Month"] = (
            monthly_df["date"]
            .dt.to_period("M")
            .dt.to_timestamp()
        )

        monthly_reviews = (
            monthly_df.groupby("Month")
            .size()
            .reset_index(name="Review Count")
            .sort_values("Month")
        )

        monthly_rating = (
            monthly_df.groupby("Month")["stars_review"]
            .mean()
            .reset_index(name="Average Rating")
            .sort_values("Month")
        )

        col1, col2 = st.columns(2)

        with col1:
            fig_monthly_reviews = px.line(
                monthly_reviews,
                x="Month",
                y="Review Count",
                markers=True,
                title="Number of Reviews Over Time"
            )

            st.plotly_chart(
                fig_monthly_reviews,
                use_container_width=True
            )

        with col2:
            fig_monthly_rating = px.line(
                monthly_rating,
                x="Month",
                y="Average Rating",
                markers=True,
                title="Average Rating Over Time"
            )

            fig_monthly_rating.update_layout(
                yaxis=dict(range=[0, 5])
            )

            st.plotly_chart(
                fig_monthly_rating,
                use_container_width=True
            )
    else:
        st.info("No valid dates are available for monthly analysis.")
else:
    st.info("The dataset does not contain a date column.")

# ============================================================
# 12. STATE ANALYSIS
# ============================================================

st.header("🗺️ Geographical Analysis")

if "state" in filtered_df.columns:
    state_df = filtered_df.dropna(
        subset=["state"]
    ).copy()

    if not state_df.empty:
        state_summary = (
            state_df.groupby("state")
            .agg(
                Total_Reviews=("state", "size"),
                Average_Rating=("stars_review", "mean")
            )
            .reset_index()
            .sort_values(
                "Total_Reviews",
                ascending=False
            )
        )

        col1, col2 = st.columns(2)

        with col1:
            top_states = state_summary.head(10)

            fig_state_reviews = px.bar(
                top_states,
                x="state",
                y="Total_Reviews",
                text="Total_Reviews",
                title="Top 10 States by Review Count",
                labels={
                    "state": "State",
                    "Total_Reviews": "Number of Reviews"
                }
            )

            st.plotly_chart(
                fig_state_reviews,
                use_container_width=True
            )

        with col2:
            state_ratings = (
                state_summary
                .dropna(subset=["Average_Rating"])
                .sort_values(
                    "Average_Rating",
                    ascending=False
                )
                .head(10)
            )

            fig_state_rating = px.bar(
                state_ratings,
                x="state",
                y="Average_Rating",
                text="Average_Rating",
                title="Top 10 States by Average Rating",
                labels={
                    "state": "State",
                    "Average_Rating": "Average Rating"
                }
            )

            fig_state_rating.update_traces(
                texttemplate="%{text:.2f}"
            )

            fig_state_rating.update_layout(
                yaxis=dict(range=[0, 5])
            )

            st.plotly_chart(
                fig_state_rating,
                use_container_width=True
            )

        st.subheader("State Performance Table")

        st.dataframe(
            state_summary.style.format({
                "Average_Rating": "{:.2f}"
            }),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No state information is available for these filters.")

# ============================================================
# 13. CITY ANALYSIS
# ============================================================

if "city" in filtered_df.columns:
    st.subheader("🏙️ City-Level Feedback")

    city_df = filtered_df.dropna(
        subset=["city"]
    ).copy()

    if not city_df.empty:
        city_summary = (
            city_df.groupby("city")
            .agg(
                Total_Reviews=("city", "size"),
                Average_Rating=("stars_review", "mean")
            )
            .reset_index()
            .sort_values(
                "Total_Reviews",
                ascending=False
            )
        )

        top_cities = city_summary.head(10)

        fig_city = px.bar(
            top_cities,
            x="city",
            y="Total_Reviews",
            text="Total_Reviews",
            title="Top 10 Cities by Review Count",
            labels={
                "city": "City",
                "Total_Reviews": "Number of Reviews"
            }
        )

        st.plotly_chart(
            fig_city,
            use_container_width=True
        )

        st.dataframe(
            city_summary.style.format({
                "Average_Rating": "{:.2f}"
            }),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No city information is available for these filters.")

# ============================================================
# 14. SENTIMENT BY STAR RATING
# ============================================================

st.header("🔍 Sentiment and Star Rating Comparison")

comparison_df = filtered_df[
    filtered_df["rating_review"].isin(valid_sentiments)
    & filtered_df["stars_review"].notna()
].copy()

if not comparison_df.empty:
    sentiment_rating = (
        comparison_df.groupby(
            ["stars_review", "rating_review"]
        )
        .size()
        .reset_index(name="Review Count")
    )

    fig_comparison = px.bar(
        sentiment_rating,
        x="stars_review",
        y="Review Count",
        color="rating_review",
        barmode="group",
        title="Sentiment Labels Across Star Ratings",
        labels={
            "stars_review": "Star Rating",
            "Review Count": "Number of Reviews",
            "rating_review": "Sentiment"
        }
    )

    st.plotly_chart(
        fig_comparison,
        use_container_width=True
    )

    st.caption(
        "This chart compares the existing sentiment labels "
        "with star ratings. It does not generate new sentiment labels."
    )
else:
    st.info(
        "There is not enough valid rating and sentiment data "
        "for this comparison."
    )



# ============================================================
# 16. FILTERED REVIEW DETAILS
# ============================================================

st.header("📝 Review Details")

display_columns = [
    col for col in [
        "Sl No",
        "date",
        "name",
        "text",
        "stars_review",
        "rating_review",
        "city",
        "state",
        "categories"
    ]
    if col in filtered_df.columns
]

st.write(
    f"Showing {len(filtered_df):,} records matching your filters."
)

st.dataframe(
    filtered_df[display_columns],
    use_container_width=True,
    hide_index=True
)

# ============================================================
# 17. DOWNLOAD FILTERED DATA
# ============================================================

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Reviews as CSV",
    data=csv_data,
    file_name="filtered_customer_feedback.csv",
    mime="text/csv"
)

# ============================================================
# 18. FOOTER
# ============================================================

st.divider()

st.caption(
    "Customer Feedback Analytics | "
    "Source: customer_feedback_cleaned.csv | "
    "Sentiment source field: rating_review"
)
