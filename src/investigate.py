import pandas as pd

FILE_PATH = "../data/processed/retail_cleaned.csv"


def load_data():
    return pd.read_csv(
        FILE_PATH,
        parse_dates=["invoicedate"]
    )


def investigate(df):

    print("\n========== NEGATIVE PRICE ==========")

    negative_price = df[df["price"] < 0]

    print("Rows:", len(negative_price))
    print(
        negative_price[
            [
                "invoice",
                "stockcode",
                "description",
                "quantity",
                "invoicedate",
                "price",
                "customer_id",
                "country"
            ]
        ].to_string(index=False)
    )

    print("\n========== ZERO PRICE ==========")

    zero_price = df[df["price"] == 0]

    print("Rows:", len(zero_price))

    print(
        zero_price[
            [
                "invoice",
                "stockcode",
                "description",
                "quantity",
                "invoicedate",
                "price",
                "customer_id",
                "country"
            ]
        ].head(30).to_string(index=False)
    )

    print("\n========== NEGATIVE QUANTITY ==========")

    negative_quantity = df[df["quantity"] < 0]

    print("Rows:", len(negative_quantity))

    print(
        negative_quantity[
            [
                "invoice",
                "stockcode",
                "description",
                "quantity",
                "price",
                "is_cancelled",
                "customer_id"
            ]
        ].head(30).to_string(index=False)
    )


if __name__ == "__main__":

    df = load_data()

    print("Loaded shape:", df.shape)

    investigate(df)