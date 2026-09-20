import pandas as pd

FILE_PATH = "../data/raw/online_retail_II.xlsx"
OUTPUT_PATH = "../data/processed/retail_cleaned.csv"


def load_data():
    sheets = pd.read_excel(FILE_PATH, sheet_name=None)
    df = pd.concat(sheets.values(), ignore_index=True)

    return df


def clean_data(df):

    # Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Remove exact duplicate rows
    df = df.drop_duplicates().copy()

    # Clean text fields
    df["description"] = df["description"].str.strip()
    df["country"] = df["country"].str.strip()
    df["stockcode"] = df["stockcode"].astype(str).str.strip()
    df["invoice"] = df["invoice"].astype(str).str.strip()

    # Identify cancellations
    df["is_cancelled"] = df["invoice"].str.startswith("C")

    # Flag negative quantity
    df["is_negative_quantity"] = df["quantity"] < 0

    # Flag zero price
    df["is_zero_price"] = df["price"] == 0

    # Flag invalid negative price
    df["is_invalid_price"] = df["price"] < 0

    # Revenue
    df["revenue"] = df["quantity"] * df["price"]

    # Customer ID as nullable integer
    df["customer_id"] = df["customer_id"].astype("Int64")

    return df


def save_data(df):

    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print("\n========== CLEANING COMPLETE ==========")
    print("Final shape:", df.shape)
    print("Saved to:", OUTPUT_PATH)


if __name__ == "__main__":

    df = load_data()

    print("Raw shape:", df.shape)

    df = clean_data(df)

    save_data(df)