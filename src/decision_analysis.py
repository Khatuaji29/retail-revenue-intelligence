import pandas as pd
import numpy as np

INPUT_PATH = "../data/processed/retail_analytical.csv"


def load_data():

    return pd.read_csv(
        INPUT_PATH,
        parse_dates=["invoicedate"],
        low_memory=False
    )


# =========================================================
# 1. CUSTOMER SEGMENT DEEP DIVE
# =========================================================

def customer_segment_analysis(df):

    sales = df[
        (df["is_sales"]) &
        (df["customer_id"].notna())
    ].copy()

    result = (
        sales
        .groupby(
            ["customer_id", "customer_segment"]
        )
        .agg(
            revenue=("sales_revenue", "sum"),
            orders=("invoice", "nunique"),
            quantity=("quantity", "sum"),
            last_purchase=("invoicedate", "max")
        )
        .reset_index()
    )

    summary = (
        result
        .groupby("customer_segment")
        .agg(
            customers=("customer_id", "nunique"),
            revenue=("revenue", "sum"),
            orders=("orders", "sum"),
            avg_customer_revenue=("revenue", "mean"),
            avg_orders=("orders", "mean")
        )
        .reset_index()
    )

    summary["revenue_share"] = (
        summary["revenue"] /
        summary["revenue"].sum() * 100
    )

    return result, summary


# =========================================================
# 2. PRODUCT RETURN RISK
# =========================================================

def product_return_analysis(df):

    sales = df[
        (df["is_sales"]) &
        (df["customer_id"].notna())
    ].copy()

    returns = df[
        (df["is_return"]) &
        (df["price"] > 0)
    ].copy()

    product_sales = (
        sales
        .groupby(["stockcode", "description"])
        .agg(
            revenue=("sales_revenue", "sum"),
            sold_quantity=("quantity", "sum"),
            orders=("invoice", "nunique"),
            customers=("customer_id", "nunique")
        )
        .reset_index()
    )

    product_returns = (
        returns
        .groupby("stockcode")
        .agg(
            returned_quantity=("quantity", lambda x: x.abs().sum()),
            return_value=("revenue", lambda x: x.abs().sum())
        )
        .reset_index()
    )

    result = product_sales.merge(
        product_returns,
        on="stockcode",
        how="left"
    )

    result["returned_quantity"] = (
        result["returned_quantity"].fillna(0)
    )

    result["return_value"] = (
        result["return_value"].fillna(0)
    )

    result["return_rate"] = (
        result["returned_quantity"] /
        result["sold_quantity"] * 100
    )

    result["return_value_rate"] = (
        result["return_value"] /
        result["revenue"] * 100
    )

    return result


# =========================================================
# 3. COUNTRY OPPORTUNITY
# =========================================================

def country_opportunity(df):

    sales = df[
        (df["is_sales"]) &
        (df["customer_id"].notna())
    ].copy()

    country = (
        sales
        .groupby("country")
        .agg(
            revenue=("sales_revenue", "sum"),
            customers=("customer_id", "nunique"),
            orders=("invoice", "nunique")
        )
        .reset_index()
    )

    country["aov"] = (
        country["revenue"] /
        country["orders"]
    )

    country["revenue_per_customer"] = (
        country["revenue"] /
        country["customers"]
    )

    return country.sort_values(
        "revenue",
        ascending=False
    )


# =========================================================
# 4. MONTHLY REVENUE DRIVER
# =========================================================

def monthly_driver_analysis(df):

    sales = df[
        (df["is_sales"]) &
        (df["customer_id"].notna())
    ].copy()

    monthly = (
        sales
        .assign(
            month=sales["invoicedate"]
            .dt.to_period("M")
            .astype(str)
        )
        .groupby("month")
        .agg(
            revenue=("sales_revenue", "sum"),
            orders=("invoice", "nunique"),
            customers=("customer_id", "nunique"),
            quantity=("quantity", "sum")
        )
        .reset_index()
    )

    monthly["aov"] = (
        monthly["revenue"] /
        monthly["orders"]
    )

    monthly["revenue_growth"] = (
        monthly["revenue"].pct_change() * 100
    )

    monthly["order_growth"] = (
        monthly["orders"].pct_change() * 100
    )

    monthly["customer_growth"] = (
        monthly["customers"].pct_change() * 100
    )

    monthly["aov_growth"] = (
        monthly["aov"].pct_change() * 100
    )

    return monthly


# =========================================================
# MAIN
# =========================================================

def main():

    df = load_data()

    print("Dataset:", df.shape)

    # -----------------------------------------------------
    # CUSTOMER SEGMENTS
    # -----------------------------------------------------

    print("\n========== CUSTOMER SEGMENT ECONOMICS ==========")

    customers, segments = customer_segment_analysis(df)

    print(
        segments.to_string(index=False)
    )

    # -----------------------------------------------------
    # PRODUCT RETURNS
    # -----------------------------------------------------

    print("\n========== HIGH-REVENUE PRODUCTS WITH RETURNS ==========")

    products = product_return_analysis(df)

    high_revenue = products[
        products["revenue"] > products["revenue"].quantile(0.90)
    ].copy()

    print(
        high_revenue
        .sort_values(
            "return_value_rate",
            ascending=False
        )
        .head(20)
        .to_string(index=False)
    )

    # -----------------------------------------------------
    # COUNTRY OPPORTUNITY
    # -----------------------------------------------------

    print("\n========== COUNTRY OPPORTUNITY ==========")

    countries = country_opportunity(df)

    print(
        countries
        .sort_values(
            "aov",
            ascending=False
        )
        .head(15)
        .to_string(index=False)
    )

    # -----------------------------------------------------
    # MONTHLY DRIVERS
    # -----------------------------------------------------

    print("\n========== MONTHLY DRIVERS ==========")

    monthly = monthly_driver_analysis(df)

    print(
        monthly.tail(12)
        .to_string(index=False)
    )

    # -----------------------------------------------------
    # SAVE
    # -----------------------------------------------------

    customers.to_csv(
        "../data/processed/customer_deep_dive.csv",
        index=False
    )

    products.to_csv(
        "../data/processed/product_return_analysis.csv",
        index=False
    )

    countries.to_csv(
        "../data/processed/country_opportunity.csv",
        index=False
    )

    monthly.to_csv(
        "../data/processed/monthly_drivers.csv",
        index=False
    )

    print("\n========== DECISION ANALYSIS COMPLETE ==========")


if __name__ == "__main__":
    main()