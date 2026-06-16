import pandas as pd
import numpy as np

# Load data
elasticity_df = pd.read_csv('../data/elasticity_scores.csv')
price_history = pd.read_csv('../data/price_history.csv')
velocity_df = pd.read_csv('../data/processed_velocity.csv')

# Get current price per SKU (most recent week)
current_prices = (
    price_history.sort_values('week')
    .groupby('sku_id')
    .last()
    .reset_index()[['sku_id', 'price', 'units_sold']]
    .rename(columns={'price': 'current_price', 'units_sold': 'current_units'})
)

# Merge all data
df = elasticity_df.merge(current_prices, on='sku_id')
df = df.merge(velocity_df[['sku_id', 'sales_velocity', 'inventory_age_days', 'red_flag']], on='sku_id')

# Holding cost assumption
HOLDING_COST_PER_UNIT_PER_WEEK = 0.50
TARGET_WEEKS_TO_CLEAR = 8

records = []

for _, row in df.iterrows():
    sku_id = row['sku_id']
    category = row['category']
    elasticity = row['elasticity_score']
    current_price = row['current_price']
    current_units = row['current_units']
    age_days = row['inventory_age_days']

    best_scenario = None
    best_revenue = -np.inf

    for discount_pct in np.linspace(0.05, 0.40, 20):
        new_price = round(current_price * (1 - discount_pct), 2)
        projected_units = int(current_units * ((new_price / current_price) ** elasticity))
        projected_units = max(projected_units, 1)

        projected_revenue = new_price * projected_units
        holding_cost_savings = HOLDING_COST_PER_UNIT_PER_WEEK * projected_units * TARGET_WEEKS_TO_CLEAR
        adjusted_revenue = projected_revenue + holding_cost_savings

        if adjusted_revenue > best_revenue:
            best_revenue = adjusted_revenue
            best_scenario = {
                'sku_id': sku_id,
                'category': category,
                'elasticity_score': elasticity,
                'current_price': current_price,
                'recommended_price': new_price,
                'discount_pct': round(discount_pct * 100, 1),
                'projected_units_sold': projected_units,
                'projected_revenue': round(projected_revenue, 2),
                'projected_margin_lift_pct': round(
                    ((adjusted_revenue - (current_price * current_units)) / 
                    max(current_price * current_units, 1)) * 100, 2
                ),
                'urgency_flag': (
                    'IMMEDIATE' if age_days > 63 and row['red_flag']
                    else 'MONITOR' if row['red_flag']
                    else 'HOLD'
                )
            }

    if best_scenario:
        records.append(best_scenario)

recommendations = pd.DataFrame(records)

print(recommendations.shape)
print(recommendations['urgency_flag'].value_counts())
print(recommendations.head())

recommendations.to_csv('../data/markdown_recommendations.csv', index=False)