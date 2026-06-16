import pandas as pd
from sqlalchemy import create_engine

# Connection
engine = create_engine('postgresql://postgres:123@localhost:5432/fashion_elasticity')

# Load CSVs
price_history = pd.read_csv('../data/price_history.csv')
velocity_df = pd.read_csv('../data/processed_velocity.csv')
recommendations = pd.read_csv('../data/markdown_recommendations.csv')

# --- dim_products ---
dim_products = recommendations[['sku_id', 'category']].drop_duplicates()
dim_products.to_sql('dim_products', engine, if_exists='append', index=False)
print(f"dim_products loaded: {len(dim_products)} rows")

# --- fact_weekly_sales ---
fact_weekly_sales = price_history.merge(
    velocity_df[['sku_id', 'sales_velocity', 'inventory_age_days']],
    on='sku_id'
).rename(columns={'week': 'week_id'})

fact_weekly_sales = fact_weekly_sales[[
    'week_id', 'sku_id', 'price', 'units_sold', 'sales_velocity', 'inventory_age_days'
]]
fact_weekly_sales.to_sql('fact_weekly_sales', engine, if_exists='append', index=False)
print(f"fact_weekly_sales loaded: {len(fact_weekly_sales)} rows")

# --- fact_markdown_recommendations ---
fact_recommendations = recommendations[[
    'sku_id', 'elasticity_score', 'current_price', 'recommended_price',
    'discount_pct', 'projected_units_sold', 'projected_revenue',
    'projected_margin_lift_pct', 'urgency_flag'
]]
fact_recommendations.to_sql('fact_markdown_recommendations', engine, if_exists='append', index=False)
print(f"fact_markdown_recommendations loaded: {len(fact_recommendations)} rows")

print("All tables loaded successfully.")