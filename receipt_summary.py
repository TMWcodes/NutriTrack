import pandas as pd

CLEANED_FILE = "Receipts_database_cleaned.xlsx"

def main():
    print("=== RECEIPT SUMMARY ===")

    # Step 1: Load cleaned receipts
    try:
        df = pd.read_excel(CLEANED_FILE)
    except FileNotFoundError:
        raise SystemExit(f"❌ {CLEANED_FILE} not found. Run update_receipt_lookup.py first.")

    # Step 2: Basic stats
    total_rows = len(df)
    unique_items = df['item_clean'].nunique()
    total_spend = df['total_value'].sum()

    # Step 3: Top items
    most_frequent = (
        df.groupby('item_clean')
          .agg(
              count=('item_clean', 'size'),
              total_quantity=('quantity', 'sum'),
              total_spend=('total_value', 'sum')
          )
          .sort_values('count', ascending=False)
          .head(10)
    )

    # Step 4: Spending over time
    spend_by_month = (
        df.groupby(df['date'].dt.to_period('M'))['total_value']
          .sum()
          .reset_index()
          .rename(columns={'date': 'month', 'total_value': 'monthly_spend'})
    )

    # Step 5: Print summary
    print(f"Total rows: {total_rows}")
    print(f"Unique items: {unique_items}")
    print(f"Total spend: £{total_spend:,.2f}")
    print("\nMost frequent items:")
    print(most_frequent)
    print("\nMonthly spend trend:")
    print(spend_by_month)

    # (Optional) Save summaries
    with pd.ExcelWriter("Receipt_Summary.xlsx") as writer:
        df.to_excel(writer, sheet_name="Cleaned Receipts", index=False)
        most_frequent.to_excel(writer, sheet_name="Top Items")
        spend_by_month.to_excel(writer, sheet_name="Monthly Spend", index=False)

    print("\n✅ Summary saved to Receipt_Summary.xlsx")


if __name__ == "__main__":
    main()
