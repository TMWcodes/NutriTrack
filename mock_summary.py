# mock_summary.py

import pandas as pd
from utils import pick_file_gui
from price_analysis_mock import (
    calculate_weighted_averages,
    plot_item_prices,
    get_top_items_with_quantity_and_value,
    get_top_selling_items,
    unique_items
)

FINAL_CLEANED_FILE = "mock_cleaned.xlsx"  # The single cleaned file with codes

def main():
    print("=== MOCK STATEMENTS SUMMARY ===")

    # Step 1: Load cleaned mock statements
    try:
        df = pd.read_excel(FINAL_CLEANED_FILE)
    except FileNotFoundError:
        raise SystemExit(f"❌ {FINAL_CLEANED_FILE} not found. Run build_mock_data.py first.")

    # Step 1a: Ensure 'name' exists for analysis
    df['name'] = df['name_clean']

    # Step 2: Weighted price trends
    price_trends = calculate_weighted_averages(df)

    # Step 3: Summary statistics
    num_unique = unique_items(df)
    print(f"\n🧾 Number of Unique Items Traded: {num_unique}")

    top_items = get_top_items_with_quantity_and_value(df, n=5)
    print("\n📦 Top 5 Most Frequently Traded Items (with Quantity & Value):")
    print(top_items)

    top_sales = get_top_selling_items(df, n=5)
    print("\n💰 Top 5 Items by Total Sales (£):")
    print(top_sales)

    # Step 4: Optional price trend plot
    search_term = input("\n🔍 Enter item name to plot trends (or leave blank to skip): ").strip()
    if search_term:
        plot_item_prices(price_trends, search_term)
    else:
        print("No item entered. Skipping plot.")

if __name__ == "__main__":
    main()
