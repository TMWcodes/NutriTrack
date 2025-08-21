from data_cleaner import clean_receipts, create_stable_lookup

def main():
    # Step 1: Clean raw receipts
    df = clean_receipts("Receipts_database.xlsx")

    # Step 2: Update lookup table
    lookup_df = create_stable_lookup(df, "item_lookup.xlsx")

    # Step 3: Detect & report potential conflicts
    print("\n⚠ Checking for potential conflicts...\n")
    # For each store/item_clean, check if multiple product codes exist
    grouped = lookup_df.groupby(['store', 'item_clean'])
    for (store, item_clean), group in grouped:
        codes = group['productCode'].dropna().unique()
        if len(codes) > 1:
            print(f"⚠ Multiple codes for '{item_clean}' (store: {store}): {list(codes)}")

    # Step 4: Summary stats
    total_rows = len(df)
    unique_items = df['item_clean'].nunique()
    most_frequent = df.groupby('item_clean').agg(
        count=('item_clean', 'size'),
        total_quantity=('quantity', 'sum'),
        total_spend=('total_value', 'sum')
    ).sort_values('count', ascending=False).head(10)

    # Step 5: Output summary
    print("\n===== RECEIPT SUMMARY =====")
    print(f"Total rows: {total_rows}")
    print(f"Number of unique items: {unique_items}")
    print("\nMost frequent items (with quantity & spend):")
    print(most_frequent)

    # Save cleaned receipts
    df.to_excel("Receipts_database_cleaned.xlsx", index=False)
    print("\n✅ Cleaned receipts saved as Receipts_database_cleaned.xlsx")
    print("✅ Lookup table updated at item_lookup.xlsx")


if __name__ == "__main__":
    main()
