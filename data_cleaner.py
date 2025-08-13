import pandas as pd

def clean_receipts(file_path):
    """Load and clean receipts data from Excel."""
    df = pd.read_excel(file_path)

    # Clean headers
    df.columns = df.columns.str.strip()

    # Convert date column
    df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')

    # Convert numeric columns
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')

    # Drop rows missing critical info
    df = df.dropna(subset=['item', 'date', 'price', 'quantity'])

    # Fill missing category and name
    df['category'] = df['category'].fillna('Uncategorized')
    df['name'] = df['name'].fillna(df['item'])

    # Compute total value
    df['total_value'] = df['price'] * df['quantity']

    # Sort by date
    df = df.sort_values('date').reset_index(drop=True)

    return df


def create_lookup_with_filled_codes(df):
    """Create item-productCode lookup, filling missing codes if one known code exists per item."""
    lookup_df = df[['item', 'productCode']].drop_duplicates().copy()

    def fill_code(group):
        codes = group['productCode'].dropna().unique()
        if len(codes) == 1:
            # Create a copy to avoid SettingWithCopyWarning
            group = group.copy()
            group['productCode'] = group['productCode'].fillna(codes[0])
        return group

    lookup_df = lookup_df.groupby('item', group_keys=False).apply(fill_code)

    # Drop rows where productCode is still missing after filling
    lookup_df = lookup_df.dropna(subset=['productCode']).reset_index(drop=True)

    return lookup_df
