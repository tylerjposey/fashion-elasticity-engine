import pandas as pd

# Load data
transactions = pd.read_csv('../data/clean_transactions.csv')
price_history = pd.read_csv('../data/price_history.csv')

# --- Sales Velocity ---
# Units sold per SKU per week
velocity = (
    price_history.groupby(['sku_id', 'category'])['units_sold']
    .sum()
    .reset_index()
)

weeks_per_sku = price_history.groupby('sku_id')['week'].max().reset_index()
weeks_per_sku.columns = ['sku_id', 'weeks_on_market']

velocity = velocity.merge(weeks_per_sku, on='sku_id')
velocity['sales_velocity'] = velocity['units_sold'] / velocity['weeks_on_market']

# --- Inventory Aging ---
# Simulate days since launch using weeks on market
velocity['inventory_age_days'] = velocity['weeks_on_market'] * 7

# --- Red Flag Logic ---
category_median_velocity = velocity.groupby('category')['sales_velocity'].median()
velocity['median_velocity'] = velocity['category'].map(category_median_velocity)

velocity['red_flag'] = (
    (velocity['sales_velocity'] < velocity['median_velocity']) &
    (velocity['inventory_age_days'] > 60)
)

# --- Export ---
velocity.to_csv('../data/processed_velocity.csv', index=False)

print(velocity.shape)
print(velocity['red_flag'].value_counts())
print(velocity.head())