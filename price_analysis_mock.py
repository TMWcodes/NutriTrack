import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------------
# Load and clean raw Excel data
# ----------------------------------------
def load_and_clean_data(file_path):
    """Loads, parses, and cleans the dataset from an Excel file."""
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip()

    # Parse date and clean price formatting
    df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
    df['price'] = df['price'].replace('[£,]', '', regex=True).astype(float)

    # Drop rows missing critical info
    df = df.dropna(subset=['name', 'date', 'quantity', 'price'])

    # Clean and normalize 'state' values
    df['state'] = df['state'].str.upper().str.strip()

    # Remove irrelevant/cancelled entries
    exclude_states = ['SELLING', 'BUYING', 'CANCELLED_BUY', 'CANCELLED_SELL']
    df = df[~df['state'].isin(exclude_states)]

    # Optional sanity checks
    if not df[df['quantity'] <= 0].empty:
        print("Warning: Quantities <= 0 found.")
    if not df[(df['price'] <= 0) | (df['price'].isna())].empty:
        print("Warning: Prices <= 0 or null found.")

    return df

# ----------------------------------------
# Monthly weighted average unit prices
# ----------------------------------------
def calculate_weighted_averages(df):
    """Computes weighted average unit prices for bought and sold items by month."""
    bought = df[df['state'] == 'BOUGHT']
    sold = df[df['state'] == 'SOLD']

    bought_monthly = (
        bought
        .groupby([bought['name'], bought['date'].dt.to_period('M')])
        .apply(lambda x: (x['price'] * x['quantity']).sum() / x['quantity'].sum())
        .reset_index(name='weighted_avg_bought_price')
    )

    sold_monthly = (
        sold
        .groupby([sold['name'], sold['date'].dt.to_period('M')])
        .apply(lambda x: (x['price'] * x['quantity']).sum() / x['quantity'].sum())
        .reset_index(name='weighted_avg_sold_price')
    )

    price_trends = pd.merge(bought_monthly, sold_monthly, on=['name', 'date'], how='outer')
    price_trends.rename(columns={'date': 'month'}, inplace=True)
    price_trends['month'] = price_trends['month'].dt.to_timestamp()

    return price_trends

# ----------------------------------------
# Plot price trends for a specific item
# ----------------------------------------
def plot_item_prices(price_trends, search_term):
    """Displays a line plot of price trends for items matching the search term."""
    matches = price_trends[price_trends['name'].str.lower().str.contains(search_term.lower())]

    if matches.empty:
        print(f"No items found matching: {search_term}")
        return

    for item in matches['name'].unique():
        df_item = matches[matches['name'] == item].sort_values('month')

        plt.figure(figsize=(10, 5))
        plt.plot(df_item['month'], df_item['weighted_avg_bought_price'], marker='o', label='Weighted Avg Bought Price')
        plt.plot(df_item['month'], df_item['weighted_avg_sold_price'], marker='o', label='Weighted Avg Sold Price')

        plt.title(f'Monthly Weighted Avg Prices for {item}')
        plt.ylabel('Price (£)')
        plt.xlabel('Month')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

# ----------------------------------------
# Top N most frequently traded items
# ----------------------------------------


def get_top_items_with_quantity_and_value(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Returns the top N most frequently traded items with:
    - trade count
    - total quantity traded
    - total sales value (price * quantity)
    """
    df['total_line_value'] = df['price'] * df['quantity']

    top = (
        df.groupby('name')
        .agg(
            trade_count=('name', 'count'),
            total_quantity=('quantity', 'sum'),
            total_value=('total_line_value', 'sum')
        )
        .sort_values('trade_count', ascending=False)
        .head(n)
    )

    # Format currency
    top['total_value'] = top['total_value'].apply(lambda x: f"£{x:,.2f}")
    return top


# ----------------------------------------
# Top N items by total revenue from sales
# ----------------------------------------
def get_top_selling_items(df, n=20):
    """
    Returns the top N items by total sales value (£).
    """
    sold_df = df[df['state'] == 'SOLD'].copy()
    sold_df['total_sale'] = sold_df['price'] * sold_df['quantity']

    return (
        sold_df.groupby('name')['total_sale']
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .apply(lambda x: f"£{x:,.2f}")
    )

# ----------------------------------------
# Total number of unique items traded
# ----------------------------------------
def unique_items(df):
    """Returns the count of unique item names."""
    return df['name'].nunique()

# ----------------------------------------
# Top N items by total quantity (sold/bought)
# ----------------------------------------
