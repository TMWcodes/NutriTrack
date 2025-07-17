# price_analysis_ge.py

import pandas as pd
import matplotlib.pyplot as plt

def load_and_clean_data(file_path):
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip()

    df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
    df['price'] = df['price'].replace('[£,]', '', regex=True).astype(float)

    df = df.dropna(subset=['name', 'date', 'quantity', 'price'])

    exclude_states = ['SELLING', 'BUYING', 'CANCELLED_BUY', 'CANCELLED_ SELL']
    df = df[~df['state'].str.upper().str.strip().isin(exclude_states)]

    # Basic data checks
    if not df[df['quantity'] <= 0].empty:
        print("Warning: Quantities <= 0 found.")
    if not df[(df['price'] <= 0) | (df['price'].isna())].empty:
        print("Warning: Prices <= 0 or null found.")

    return df

def calculate_weighted_averages(df):
    bought = df[df['state'].str.upper() == 'BOUGHT']
    sold = df[df['state'].str.upper() == 'SOLD']

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

def plot_item_prices(price_trends, search_term):
    matches = price_trends[price_trends['name'].str.lower().str.contains(search_term.lower())]

    if matches.empty:
        print(f"No items found matching: {search_term}")
    else:
        for item in matches['name'].unique():
            df_item = matches[matches['name'] == item]
            df_item = df_item.sort_values('month')

            plt.figure(figsize=(10,5))
            plt.plot(df_item['month'], df_item['weighted_avg_bought_price'], marker='o', label='Weighted Avg Bought Price')
            plt.plot(df_item['month'], df_item['weighted_avg_sold_price'], marker='o', label='Weighted Avg Sold Price')

            plt.title(f'Monthly Weighted Avg Prices for {item}')
            plt.ylabel('Price (£)')
            plt.xlabel('Month')
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.show()
