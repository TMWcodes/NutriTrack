import pandas as pd
from data_cleaner import clean_receipts, create_lookup_table, merge_codes_by_item_clean

RECEIPTS_FILE = "Receipts_database.xlsx"
LOOKUP_FILE = "item_lookup.xlsx"
CLEANED_FILE = "Receipts_cleaned.xlsx"

def main():
    print("=== STEP 1: Load and clean raw receipts ===")
    df_clean = clean_receipts(RECEIPTS_FILE)
    print(f"✅ Cleaned {len(df_clean)} receipts")
    print(df_clean.head())

    print("\n=== STEP 2: Update lookup table ===")
    lookup_df = create_lookup_table(df_clean, lookup_path=LOOKUP_FILE)
    print(f"✅ Lookup table now has {len(lookup_df)} entries")
    print(lookup_df.head())

    print("\n=== STEP 3: Merge lookup codes into cleaned receipts ===")
    df_final = merge_codes_by_item_clean(df_clean, lookup_path=LOOKUP_FILE)
    print(f"✅ Codes merged into cleaned receipts")
    print(df_final.head())

    print("\n=== STEP 4: Save cleaned receipts with codes ===")
    with pd.ExcelWriter(CLEANED_FILE, engine="openpyxl") as writer:
        df_final.to_excel(writer, index=False, sheet_name="Receipts")

    print(f"🎉 All done! Cleaned receipts saved to {CLEANED_FILE}")

if __name__ == "__main__":
    main()
