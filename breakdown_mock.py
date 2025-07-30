# breakdown_mock.py

import sys
import pandas as pd
from utils import pick_file_gui  # Reusable file picker function

# Import custom analysis functions
from price_analysis_mock import (
    load_and_clean_data,
    calculate_weighted_averages,
    plot_item_prices,
    get_top_items_with_quantity_and_value,
    get_top_selling_items,
    unique_items
)

# ---------------------------------------
# Step 1: Select file (via CLI or GUI)
# ---------------------------------------
if len(sys.argv) > 1:
    file_path = sys.argv[1]
else:
    print("No file path provided. Please choose a file.")
    file_path = pick_file_gui()

if not file_path:
    print("No file selected. Exiting.")
    sys.exit()

# ---------------------------------------
# Step 2: Load and clean the data
# ---------------------------------------
df = load_and_clean_data(file_path)
price_trends = calculate_weighted_averages(df)

# ---------------------------------------
# Step 3: Summary statistics
# ---------------------------------------

# Number of unique items
num_unique = unique_items(df)
print(f"\n🧾 Number of Unique Items Traded: {num_unique}")


# Most frequently traded (with quantity)
top_items = get_top_items_with_quantity_and_value(df, n=5)
print("\n📦 Top 5 Most Frequently Traded Items (with Quantity):")
print(top_items)


# Highest total sales (value £)
top_sales = get_top_selling_items(df, n=5)
print("\n💰 Top 5 Items by Total Sales (£):")
print(top_sales)

# ---------------------------------------
# Step 4: Optional price trend plot
# ---------------------------------------
search_term = input("\n🔍 Enter item name to plot trends (or leave blank to skip): ").strip()

if search_term:
    plot_item_prices(price_trends, search_term)
else:
    print("No item entered. Skipping plot.")
