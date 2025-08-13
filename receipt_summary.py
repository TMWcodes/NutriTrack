from data_cleaner import clean_receipts

# Load cleaned data
df = clean_receipts("Receipts_database.xlsx")

# Summary stats
total_rows = len(df)
unique_items = df['item'].nunique()
most_frequent = df.groupby('item').agg(
    count=('item', 'size'),
    total_quantity=('quantity', 'sum'),
    total_spend=('total_value', 'sum')
).sort_values('count', ascending=False).head(10)

# Output
print(f"Total rows: {total_rows}")
print(f"Number of unique items: {unique_items}")
print("\nMost frequent items (with quantity & spend):")
print(most_frequent)
