import pandas as pd
import numpy as np

INPUT_PATH = "../data/processed/retail_analytical.csv"


def load_data():

    df = pd.read_csv(
        INPUT_PATH,
        parse_dates=["invoicedate"]
    )

    return df


# =========================================================
# 1. EXECUTIVE KPIs
# =========================================================

def executive_kpis(df):

    sales = df[df["is_sales"]].copy()

    revenue = sales["sales_revenue"].sum()

    orders = sales["invoice"].nunique()

    customers = sales["customer_id"].nunique()

    quantity = sales["quantity"].sum()

    aov = revenue / orders

    items_per_order = quantity / orders

    return {
        "Revenue": revenue,
        "Orders": orders,
        "Customers": customers,
        "Quantity Sold": quantity,
        "AOV": aov,
        "Items per Order": items_per_order
    }


# =========================================================
# 2. MONTHLY REVENUE
# =========================================================

def monthly_revenue(df):

    sales = df[df["is_sales"]].copy()

    monthly = (
        sales
        .groupby(
            sales["invoicedate"].dt.to_period("M")
        )
        .agg(
            revenue=("sales_revenue", "sum"),
            orders=("invoice", "nunique"),
            customers=("customer_id", "nunique")
        )
        .reset_index()
    )

    monthly["month"] = monthly["invoicedate"].astype(str)

    monthly["aov"] = (
        monthly["revenue"] /
        monthly["orders"]
    )

    monthly["mom_growth"] = (
        monthly["revenue"]
        .pct_change() * 100
    )

    return monthly


# =========================================================
# 3. COUNTRY PERFORMANCE
# =========================================================

def country_analysis(df):

    sales = df[df["is_sales"]].copy()

    country = (
        sales
        .groupby("country")
        .agg(
            revenue=("sales_revenue", "sum"),
            orders=("invoice", "nunique"),
            customers=("customer_id", "nunique"),
            quantity=("quantity", "sum")
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
# 4. CUSTOMER ANALYSIS
# =========================================================

def customer_analysis(df):

    sales = df[
        (df["is_sales"]) &
        (df["customer_id"].notna())
    ].copy()

    customers = (
        sales
        .groupby("customer_id")
        .agg(
            revenue=("sales_revenue", "sum"),
            orders=("invoice", "nunique"),
            quantity=("quantity", "sum")
        )
        .reset_index()
    )

    customers["aov"] = (
        customers["revenue"] /
        customers["orders"]
    )

    customers["revenue_share"] = (
        customers["revenue"] /
        customers["revenue"].sum()
        * 100
    )

    return customers.sort_values(
        "revenue",
        ascending=False
    )


# =========================================================
# 5. PRODUCT ANALYSIS
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

    products["revenue_share"] = (
        products["revenue"] /
        products["revenue"].sum()
        * 100
    )

    products["avg_price"] = (
        products["revenue"] /
        products["quantity"]
    )

    return products.sort_values(
        "revenue",
        ascending=False
    )


# =========================================================
# 6. PARETO ANALYSIS
# =========================================================

def pareto_analysis(products):

    products = products.sort_values(
        "revenue",
        ascending=False
    ).copy()

    products["cumulative_revenue"] = (
        products["revenue"].cumsum()
    )

    total_revenue = products["revenue"].sum()

    products["cumulative_revenue_pct"] = (
        products["cumulative_revenue"] /
        total_revenue * 100
    )

    products["cumulative_product_pct"] = (
        np.arange(1, len(products) + 1) /
        len(products) * 100
    )

    return products


# =========================================================
# 7. RETURN / CANCELLATION ANALYSIS
# =========================================================

def cancellation_analysis(df):

    total_orders = df["invoice"].nunique()

    cancelled_orders = df[
        df["is_cancelled"]
    ]["invoice"].nunique()

    cancelled_quantity = df[
        df["is_return"]
    ]["quantity"].abs().sum()

    cancelled_value = df[
        df["is_return"]
    ]["revenue"].abs().sum()

    cancellation_rate = (
        cancelled_orders /
        total_orders * 100
    )

    return {
        "Total Orders": total_orders,
        "Cancelled Orders": cancelled_orders,
        "Cancellation Rate": cancellation_rate,
        "Returned Quantity": cancelled_quantity,
        "Return Value": cancelled_value
    }


# =========================================================
# 8. NEW VS RETURNING CUSTOMERS
# =========================================================

def customer_type_analysis(df):

    sales = df[
        (df["is_sales"]) &
        (df["customer_id"].notna())
    ].copy()

    first_purchase = (
        sales
        .groupby("customer_id")["invoicedate"]
        .min()
        .rename("first_purchase")
    )

    sales = sales.merge(
        first_purchase,
        on="customer_id",
        how="left"
    )

    sales["purchase_month"] = (
        sales["invoicedate"]
        .dt.to_period("M")
    )

    sales["first_purchase_month"] = (
        sales["first_purchase"]
        .dt.to_period("M")
    )

    sales["customer_type"] = np.where(
        sales["purchase_month"] ==
        sales["first_purchase_month"],
        "New",
        "Returning"
    )

    monthly = (
        sales
        .groupby(
            ["purchase_month", "customer_type"]
        )
        .agg(
            revenue=("sales_revenue", "sum"),
            customers=("customer_id", "nunique")
        )
        .reset_index()
    )

    return monthly


# =========================================================
# MAIN ANALYSIS
# =========================================================

def main():

    print("Loading analytical dataset...")

    df = load_data()

    print("Dataset shape:", df.shape)

    # -----------------------------------------------------
    # Executive KPIs
    # -----------------------------------------------------

    print("\n========== EXECUTIVE KPIs ==========")

    kpis = executive_kpis(df)

    for key, value in kpis.items():
        print(f"{key}: {value:,.2f}")

    # -----------------------------------------------------
    # Monthly revenue
    # -----------------------------------------------------

    print("\n========== MONTHLY REVENUE ==========")

    monthly = monthly_revenue(df)

    print(monthly.tail(12).to_string(index=False))

    # -----------------------------------------------------
    # Country
    # -----------------------------------------------------

    print("\n========== TOP COUNTRIES ==========")

    countries = country_analysis(df)

    print(
        countries.head(15).to_string(
            index=False
        )
    )

    # -----------------------------------------------------
    # Customers
    # -----------------------------------------------------

    print("\n========== TOP CUSTOMERS ==========")

    customers = customer_analysis(df)

    print(
        customers.head(15).to_string(
            index=False
        )
    )

    # -----------------------------------------------------
    # Products
    # -----------------------------------------------------

    print("\n========== TOP PRODUCTS ==========")

    products = product_analysis(df)

    print(
        products.head(15).to_string(
            index=False
        )
    )

    # -----------------------------------------------------
    # Pareto
    # -----------------------------------------------------

    print("\n========== PARETO ==========")

    pareto = pareto_analysis(products)

    product_count_80 = (
        pareto[
            pareto["cumulative_revenue_pct"] <= 80
        ]
        .shape[0]
    )

    product_percentage_80 = (
        product_count_80 /
        len(pareto) * 100
    )

    print(
        f"Products generating first 80% "
        f"of revenue: {product_count_80:,}"
    )

    print(
        f"Percentage of products: "
        f"{product_percentage_80:.2f}%"
    )

    # -----------------------------------------------------
    # Cancellation
    # -----------------------------------------------------

    print("\n========== CANCELLATION ANALYSIS ==========")

    cancellation = cancellation_analysis(df)

    for key, value in cancellation.items():
        print(f"{key}: {value:,.2f}")

    # -----------------------------------------------------
    # New vs Returning
    # -----------------------------------------------------

    print("\n========== NEW VS RETURNING ==========")

    customer_types = customer_type_analysis(df)

    print(
        customer_types.tail(12).to_string(
            index=False
        )
    )


if __name__ == "__main__":
    main()