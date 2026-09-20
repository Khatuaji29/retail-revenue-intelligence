import pandas as pd

INPUT_PATH = "../data/processed/retail_cleaned.csv"
OUTPUT_PATH = "../data/processed/retail_analytical.csv"


def load_data():

    return pd.read_csv(
        INPUT_PATH,
        parse_dates=["invoicedate"]
    )


def create_features(df):

    # =====================================================
    # DATE & TIME FEATURES
    # =====================================================

    df["year"] = df["invoicedate"].dt.year
    df["month"] = df["invoicedate"].dt.month
    df["month_name"] = df["invoicedate"].dt.strftime("%b")

    # Year-Month for time-series analysis
    df["year_month"] = (
        df["invoicedate"]
        .dt.to_period("M")
        .astype(str)
    )

    # Quarter
    df["quarter"] = df["invoicedate"].dt.quarter

    # Day of week
    df["day_of_week"] = df["invoicedate"].dt.dayofweek
    df["day_name"] = df["invoicedate"].dt.strftime("%A")

    # Hour
    df["hour"] = df["invoicedate"].dt.hour

    # Weekend flag
    df["is_weekend"] = df["day_of_week"] >= 5

    # =====================================================
    # TRANSACTION CLASSIFICATION
    # =====================================================

    # Return / cancellation transaction
    df["is_return"] = df["quantity"] < 0

    # Valid sales transaction
    df["is_sales"] = (
        (df["quantity"] > 0) &
        (df["price"] > 0) &
        (~df["is_invalid_price"])
    )

    # =====================================================
    # PRODUCT CLASSIFICATION
    # =====================================================

    def classify_product(row):

        stockcode = str(row["stockcode"]).strip().upper()
        description = str(row["description"]).strip().upper()

        # Operational / service transactions
        if stockcode in {"POST", "DOT", "M"}:
            return "Operational / Service"

        if "POSTAGE" in description:
            return "Operational / Service"

        if "MANUAL" in description:
            return "Operational / Service"

        # Accounting / adjustment transactions
        if "BAD DEBT" in description:
            return "Adjustment"

        if "ADJUSTMENT" in description:
            return "Adjustment"

        return "Regular Product"

    df["product_type"] = df.apply(
        classify_product,
        axis=1
    )

    # Easy filter for product analysis
    df["is_regular_product"] = (
        df["product_type"] == "Regular Product"
    )

    # =====================================================
    # REVENUE
    # =====================================================

    df["revenue"] = (
        df["quantity"] *
        df["price"]
    )

    # Revenue from valid sales only
    df["sales_revenue"] = df["revenue"].where(
        df["is_sales"],
        0
    )

    # Return value
    df["return_value"] = df["revenue"].where(
        df["is_return"],
        0
    )

    # =====================================================
    # ORDER LEVEL
    # =====================================================

    df["order_id"] = df["invoice"].str.replace(
        "C",
        "",
        regex=False
    )

    return df


def create_rfm(df):

    # Only identifiable customers and valid sales
    customer_data = df[
        (df["customer_id"].notna()) &
        (df["is_sales"])
    ].copy()

    # Most recent transaction date in the dataset
    reference_date = customer_data["invoicedate"].max()

    # =====================================================
    # RFM METRICS
    # =====================================================

    rfm = (
        customer_data
        .groupby("customer_id")
        .agg(
            recency=(
                "invoicedate",
                lambda x: (
                    reference_date - x.max()
                ).days
            ),
            frequency=(
                "invoice",
                "nunique"
            ),
            monetary=(
                "sales_revenue",
                "sum"
            )
        )
        .reset_index()
    )

    # =====================================================
    # RFM SCORES
    # =====================================================

    # Recency:
    # Lower number of days = better customer activity
    rfm["R_score"] = pd.qcut(
        rfm["recency"],
        5,
        labels=[5, 4, 3, 2, 1],
        duplicates="drop"
    )

    # Frequency
    rfm["F_score"] = pd.qcut(
        rfm["frequency"].rank(method="first"),
        5,
        labels=[1, 2, 3, 4, 5]
    )

    # Monetary value
    rfm["M_score"] = pd.qcut(
        rfm["monetary"].rank(method="first"),
        5,
        labels=[1, 2, 3, 4, 5]
    )

    # =====================================================
    # TOTAL RFM SCORE
    # =====================================================

    rfm["RFM_score"] = (
        rfm["R_score"].astype(int) +
        rfm["F_score"].astype(int) +
        rfm["M_score"].astype(int)
    )

    # =====================================================
    # CUSTOMER SEGMENTS
    # =====================================================

    def segment(row):

        if row["RFM_score"] >= 13:
            return "Champions"

        elif row["RFM_score"] >= 10:
            return "Loyal Customers"

        elif row["RFM_score"] >= 7:
            return "Potential Loyalists"

        elif row["RFM_score"] >= 5:
            return "At Risk"

        else:
            return "Lost"

    rfm["customer_segment"] = rfm.apply(
        segment,
        axis=1
    )

    return rfm


def main():

    print("Loading cleaned data...")

    df = load_data()

    print("Rows:", len(df))

    # =====================================================
    # FEATURE ENGINEERING
    # =====================================================

    print("\nCreating analytical features...")

    df = create_features(df)

    # =====================================================
    # RFM ANALYSIS
    # =====================================================

    print("\nCreating RFM analysis...")

    rfm = create_rfm(df)

    print(
        "Customers analyzed:",
        len(rfm)
    )

    # =====================================================
    # ADD CUSTOMER FEATURES TO TRANSACTIONS
    # =====================================================

    df = df.merge(
        rfm[
            [
                "customer_id",
                "recency",
                "frequency",
                "monetary",
                "RFM_score",
                "customer_segment"
            ]
        ],
        on="customer_id",
        how="left"
    )

    # =====================================================
    # SAVE ANALYTICAL DATASET
    # =====================================================

    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    # =====================================================
    # OUTPUT SUMMARY
    # =====================================================

    print(
        "\n========== ANALYTICAL DATASET =========="
    )

    print(
        "Shape:",
        df.shape
    )

    print(
        "Saved:",
        OUTPUT_PATH
    )

    print(
        "\n========== PRODUCT TYPES =========="
    )

    print(
        df["product_type"]
        .value_counts()
    )

    print(
        "\n========== CUSTOMER SEGMENTS =========="
    )

    print(
        rfm["customer_segment"]
        .value_counts()
    )

    print(
        "\n========== FEATURE SUMMARY =========="
    )

    print(
        "Regular products:",
        df["is_regular_product"].sum()
    )

    print(
        "Sales transactions:",
        df["is_sales"].sum()
    )

    print(
        "Return transactions:",
        df["is_return"].sum()
    )

    print(
        "Weekend transactions:",
        df["is_weekend"].sum()
    )


if __name__ == "__main__":
    main()

