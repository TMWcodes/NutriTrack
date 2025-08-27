# build_mock_data.py

import pandas as pd
from utils import select_file
from mock_cleaner import clean_mock_statements, create_mock_lookup, save_cleaned

# File paths
MOCK_FILE = select_file()        # User selects input Excel file
LOOKUP_FILE = "mock_lookup.xlsx" # Stable lookup table
FINAL_CLEANED_FILE = "mock_cleaned.xlsx"  # Final cleaned file with codes

def main():
    print("=== STEP 1: Load and clean mock statements ===")
    df_clean = clean_mock_statements(MOCK_FILE)
    
    print(f"✅ Cleaned {len(df_clean)} statements")
    print(df_clean.head())

    print("\n=== STEP 2: Create/update lookup table and assign codes ===")
    df_final, lookup_df = create_mock_lookup(df_clean, lookup_path=LOOKUP_FILE)
    print(f"✅ Lookup table now has {len(lookup_df)} entries")
    print(lookup_df.head())

    print("\n=== STEP 3: Save final cleaned statements with codes ===")
    save_cleaned(df_final, output_path=FINAL_CLEANED_FILE)

if __name__ == "__main__":
    main()