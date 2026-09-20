import pandas as pd

FILE_PATH = "../data/raw/online_retail_II.xlsx"


def load_data():
    sheets = pd.read_excel(FILE_PATH, sheet_name=None)
    return pd.concat(sheets.values(), ignore_index=True)


def profile_data(df):

    print("\n========== QUANTITY ==========")
    print("Negative quantity:", (df["Quantity"] < 0).sum())
    print("Zero quantity:", (df["Quantity"] == 0).sum())
    print("Positive quantity:", (df["Quantity"] > 0).sum())

    print("\n========== PRICE ==========")
    print("Zero price:", (df["Price"] == 0).sum())
    print("Negative price:", (df["Price"] < 0).sum())
    print("Minimum price:", df["Price"].min())
    print("Maximum price:", df["Price"].max())

    print("\n========== INVOICES ==========")
    print("Unique invoices:", df["Invoice"].nunique())

    print("\n========== PRODUCTS ==========")
    print("Unique products:", df["StockCode"].nunique())

    print("\n========== CUSTOMERS ==========")
    print("Unique customers:", df["Customer ID"].nunique())

    print("\n========== COUNTRIES ==========")
    print("Unique countries:", df["Country"].nunique())
    print(df["Country"].value_counts().head(15))

    print("\n========== INVOICE PATTERN ==========")
    cancelled = df["Invoice"].astype(str).str.startswith("C")
    print("Cancellation rows:", cancelled.sum())

    print("\n========== NEGATIVE QUANTITY + CANCELLATION ==========")
    print(
        ((df["Quantity"] < 0) & cancelled).sum()
    )


if __name__ == "__main__":
    df = load_data()
    profile_data(df)