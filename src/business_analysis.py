import pandas as pd
import numpy as np

INPUT_PATH = "../data/processed/retail_analytical.csv"


def load_data():
    df = pd.read_csv(
        INPUT_PATH,
        parse_dates=["invoicedate"],
        low_memory=False
    )

    return df


# =========================================================
# 1. ORDER-LEVEL ANALYSIS
# =========================================================

def order_analysis(df):

    sales = df[
        (df["is_sales"]) &
        (df["customer_id"].notna())
    ].copy()

    orders = (
        sales
        .groupby("invoice")
        .agg(
            customer_id=("customer_id", "first"),
            order_date=("invoicedate", "min"),
            country=("country", "first"),
            revenue=("sales_revenue", "sum"),
            items=("quantity", "sum"),
            products=("stockcode", "nunique")
        )
        .reset_index()
    )

    return orders


# =========================================================
# 2. ORDER KPIs
# =========================================================

def order_kpis(orders):

    return {
        "Orders": len(orders),
        "Revenue": orders["revenue"].sum(),
        "AOV": orders["revenue"].mean(),
        "Average Items per Order": orders["items"].mean(),
        "Average Products per Order": orders["products"].mean()
    }


# =========================================================
# 3. NEW VS RETURNING CUSTOMERS
# =========================================================

def retention_analysis(orders):

    orders = orders.sort_values(
        ["customer_id", "order_date"]
    ).copy()

    orders["customer_order_number"] = (
        orders
        .groupby("customer_id")
        .cumcount() + 1
    )

    orders["customer_type"] = np.where(
        orders["customer_order_number"] == 1,
        "New",
        "Returning"
    )

    monthly = (
        orders
        .assign(
            month=orders["order_date"]
            .dt.to_period("M")
            .astype(str)
        )
        .groupby(["month", "customer_type"])
        .agg(
            revenue=("revenue", "sum"),
            orders=("invoice", "nunique"),
            customers=("customer_id", "nunique")
        )
        .reset_index()
    )

    return monthly


# =========================================================
# 4. CUSTOMER CONCENTRATION
# =========================================================

def customer_concentration(orders):

    customer = (
        orders
        .groupby("customer_id")
        .agg(
            revenue=("revenue", "sum"),
            orders=("invoice", "nunique")
        )
        .reset_index()
        .sort_values(
            "revenue",
            ascending=False
        )
    )

    total_revenue = customer["revenue"].sum()

    customer["revenue_share"] = (
        customer["revenue"] /
        total_revenue * 100
    )

    customer["cumulative_revenue"] = (
        customer["revenue"].cumsum()
    )

    customer["cumulative_revenue_pct"] = (
        customer["cumulative_revenue"] /
        total_revenue * 100
    )

    results = {}

    for percentage in [1, 5, 10, 20]:

        count = max(
            1,
            int(len(customer) * percentage / 100)
        )

        revenue_share = (
            customer
            .head(count)["revenue"]
            .sum()
            / total_revenue
            * 100
        )

        results[f"Top {percentage}% customers"] = revenue_share

    return customer, results


# =========================================================
# 5. PRODUCT PERFORMANCE
# =========================================================

def product_analysis(df):

    sales = df[df["is_sales"]].copy()

    products = (
        sales
        .groupby(["stockcode", "description"])
        .agg(
            revenue=("sales_revenue", "sum"),
            quantity=("quantity", "sum"),
            orders=("invoice", "nunique"),
            customers=("customer_id", "nunique")
        )
        .reset_index()
    )

    products["average_price"] = (
        products["revenue"] /
        products["quantity"]
    )

    products["revenue_share"] = (
        products["revenue"] /
        products["revenue"].sum()
        * 100
    )

    return products.sort_values(
        "revenue",
        ascending=False
    )


# =========================================================
# 6. RETURN / CANCELLATION ANALYSIS
# =========================================================

def return_analysis(df):

    sales = df[df["is_sales"]].copy()

    returns = df[
        (df["is_return"]) &
        (df["price"] > 0)
    ].copy()

    gross_sales = sales["sales_revenue"].sum()

    return_value = returns["revenue"].abs().sum()

    sold_quantity = sales["quantity"].sum()

    returned_quantity = returns["quantity"].abs().sum()

    return {
        "Gross Sales": gross_sales,
        "Return Value": return_value,
        "Return Value Rate": (
            return_value / gross_sales * 100
        ),
        "Sold Quantity": sold_quantity,
        "Returned Quantity": returned_quantity,
        "Quantity Return Rate": (
            returned_quantity /
            sold_quantity * 100
        ),
        "Cancelled Orders": returns["invoice"].nunique()
    }


# =========================================================
# 7. CUSTOMER SEGMENT ECONOMICS
# =========================================================

def segment_analysis(df):

    sales = df[
        (df["is_sales"]) &
        (df["customer_id"].notna())
    ].copy()

    segment = (
        sales
        .groupby(
            ["customer_id", "customer_segment"]
        )
        .agg(
            revenue=("sales_revenue", "sum"),
            orders=("invoice", "nunique")
        )
        .reset_index()
    )

    result = (
        segment
        .groupby("customer_segment")
        .agg(
            customers=("customer_id", "nunique"),
            revenue=("revenue", "sum"),
            orders=("orders", "sum")
        )
        .reset_index()
    )

    result["revenue_per_customer"] = (
        result["revenue"] /
        result["customers"]
    )

    result["revenue_share"] = (
        result["revenue"] /
        result["revenue"].sum()
        * 100
    )

    return result.sort_values(
        "revenue",
        ascending=False
    )


# =========================================================
# 8. MONTHLY GROWTH DECOMPOSITION
# =========================================================

def growth_analysis(orders):

    monthly = (
        orders
        .assign(
            month=orders["order_date"]
            .dt.to_period("M")
            .astype(str)
        )
        .groupby("month")
        .agg(
            revenue=("revenue", "sum"),
            orders=("invoice", "nunique"),
            customers=("customer_id", "nunique")
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

    monthly["aov_growth"] = (
        monthly["aov"]
        .pct_change() * 100
    )

    monthly["customer_growth"] = (
        monthly["customers"]
        .pct_change() * 100
    )

    return monthly


# =========================================================
# 9. COUNTRY OPPORTUNITY
# =========================================================

def country_analysis(orders):

    country = (
        orders
        .groupby("country")
        .agg(
            revenue=("revenue", "sum"),
            orders=("invoice", "nunique"),
            customers=("customer_id", "nunique")
        )
        .reset_index()
    )

    country["aov"] = (
        country["revenue"] /
        country["orders"]
    )

    country["revenue_share"] = (
        country["revenue"] /
        country["revenue"].sum()
        * 100
    )

    return country.sort_values(
        "revenue",
        ascending=False
    )


# =========================================================
# 10. MAIN
# =========================================================

def main():

    print("Loading analytical dataset...")

    df = load_data()

    print("Rows:", len(df))

    # -----------------------------------------------------
    # ORDER ANALYSIS
    # -----------------------------------------------------

    print("\n========== ORDER ANALYSIS ==========")

    orders = order_analysis(df)

    kpis = order_kpis(orders)

    for key, value in kpis.items():
        print(f"{key}: {value:,.2f}")

    # -----------------------------------------------------
    # RETENTION
    # -----------------------------------------------------

    print("\n========== RETENTION ==========")

    retention = retention_analysis(orders)

    print(
        retention.tail(12)
        .to_string(index=False)
    )

    # -----------------------------------------------------
    # CUSTOMER CONCENTRATION
    # -----------------------------------------------------

    print("\n========== CUSTOMER CONCENTRATION ==========")

    customers, concentration = (
        customer_concentration(orders)
    )

    for key, value in concentration.items():
        print(f"{key}: {value:.2f}%")

    # -----------------------------------------------------
    # PRODUCT
    # -----------------------------------------------------

    print("\n========== PRODUCT PERFORMANCE ==========")

    products = product_analysis(df)

    print(
        products.head(15)
        .to_string(index=False)
    )

    # -----------------------------------------------------
    # RETURNS
    # -----------------------------------------------------

    print("\n========== RETURN ANALYSIS ==========")

    returns = return_analysis(df)

    for key, value in returns.items():
        print(f"{key}: {value:,.2f}")

    # -----------------------------------------------------
    # SEGMENTS
    # -----------------------------------------------------

    print("\n========== CUSTOMER SEGMENTS ==========")

    segments = segment_analysis(df)

    print(
        segments.to_string(index=False)
    )

    # -----------------------------------------------------
    # GROWTH
    # -----------------------------------------------------

    print("\n========== GROWTH DECOMPOSITION ==========")

    growth = growth_analysis(orders)

    print(
        growth.tail(12)
        .to_string(index=False)
    )

    # -----------------------------------------------------
    # COUNTRIES
    # -----------------------------------------------------

    print("\n========== COUNTRY PERFORMANCE ==========")

    countries = country_analysis(orders)

    print(
        countries.head(15)
        .to_string(index=False)
    )

    # -----------------------------------------------------
    # SAVE OUTPUTS
    # -----------------------------------------------------

    orders.to_csv(
        "../data/processed/orders.csv",
        index=False
    )

    retention.to_csv(
        "../data/processed/retention_monthly.csv",
        index=False
    )

    customers.to_csv(
        "../data/processed/customer_analysis.csv",
        index=False
    )

    products.to_csv(
        "../data/processed/product_analysis.csv",
        index=False
    )

    growth.to_csv(
        "../data/processed/growth_analysis.csv",
        index=False
    )

    countries.to_csv(
        "../data/processed/country_analysis.csv",
        index=False
    )

    segments.to_csv(
        "../data/processed/segment_analysis.csv",
        index=False
    )

    print("\n========== ANALYSIS COMPLETE ==========")


if __name__ == "__main__":
    main()