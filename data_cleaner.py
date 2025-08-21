import pandas as pd
import os

AUTO_CODE_START = 90000000  # Reserve for auto-generated codes

def clean_receipts(file_path):
    """
    Load and clean receipts data from Excel.
    Ensures required columns exist and normalizes data.
    """
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip()  # Clean headers

    # Required columns
    required = ["store", "location", "item", "price", "quantity", "date"]
    for col in required:
        if col not in df.columns:
            raise KeyError(f"Missing required column: {col}")

    # Optional columns
    if "category" not in df.columns:
        df["category"] = "Uncategorized"
    if "name" not in df.columns:
        df["name"] = df["item"]
    if "productCode" not in df.columns:
        df["productCode"] = None

    # Convert column types
    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    # Drop rows missing critical info
    df = df.dropna(subset=["item", "date", "price", "quantity"])

    # Normalize item name
    df["item_clean"] = df["item"].str.strip().str.lower()

    # Compute total value
    df["total_value"] = df["price"] * df["quantity"]

    # Sort by date
    df = df.sort_values("date").reset_index(drop=True)
    return df


def create_stable_lookup(df, lookup_path="item_lookup.xlsx"):
    """
    Build or update a stable lookup table for items.
    Auto-generates numeric product codes if missing.
    Removes duplicates, keeps normalized item names.
    """
    # Load existing lookup if available
    if os.path.exists(lookup_path):
        lookup_df = pd.read_excel(lookup_path, dtype={"productCode": "Int64"})
    else:
        lookup_df = pd.DataFrame(columns=["store", "item_clean", "item", "productCode"])

    updated_records = []

    for _, row in df.iterrows():
        store = str(row["store"]).strip()
        item_clean = str(row["item_clean"]).strip()
        item = str(row["item"]).strip()

        # Determine productCode
        if pd.notna(row["productCode"]):
            try:
                code = int(row["productCode"])
            except ValueError:
                # Non-numeric → assign auto
                code = AUTO_CODE_START + (abs(hash(store + item_clean)) % 10000000)
        else:
            # Missing → assign auto
            code = AUTO_CODE_START + (abs(hash(store + item_clean)) % 10000000)

        # Check for existing record
        match = lookup_df[(lookup_df["store"] == store) & (lookup_df["item_clean"] == item_clean)]
        if match.empty or code not in match["productCode"].values:
            updated_records.append({
                "store": store,
                "item_clean": item_clean,
                "item": item,
                "productCode": code
            })

    # Merge and drop duplicates
    if updated_records:
        lookup_df = pd.concat([lookup_df, pd.DataFrame(updated_records)], ignore_index=True)

    # Drop exact duplicates
    lookup_df = lookup_df.drop_duplicates(subset=["store", "item_clean", "productCode"])

    # Sort by store and item_clean for readability
    lookup_df = lookup_df.sort_values(["store", "item_clean"]).reset_index(drop=True)

    # Save lookup table with adjusted column widths
    from openpyxl.utils import get_column_letter

    with pd.ExcelWriter(lookup_path, engine="openpyxl") as writer:
        lookup_df.to_excel(writer, index=False, sheet_name="Lookup")
        worksheet = writer.sheets["Lookup"]
        for i, col in enumerate(lookup_df.columns, 1):
            max_len = max(lookup_df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.column_dimensions[get_column_letter(i)].width = max_len

    return lookup_df
