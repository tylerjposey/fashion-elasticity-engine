import pandas as pd
import numpy as np
import statsmodels.api as sm

# Load price history
price_history = pd.read_csv('../data/price_history.csv')

# Remove any rows with 0 or negative values (log undefined)
price_history = price_history[(price_history['price'] > 0) & (price_history['units_sold'] > 0)]

# Log transform
price_history['log_price'] = np.log(price_history['price'])
price_history['log_units'] = np.log(price_history['units_sold'])

results = []

for sku_id, group in price_history.groupby('sku_id'):
    if len(group) < 3:  # need at least 3 data points for regression
        continue

    X = sm.add_constant(group['log_price'])
    y = group['log_units']

    try:
        model = sm.OLS(y, X).fit()
        elasticity = model.params['log_price']
        r_squared = model.rsquared

        results.append({
            'sku_id': sku_id,
            'category': group['category'].iloc[0],
            'elasticity_score': round(elasticity, 4),
            'r_squared': round(r_squared, 4)
        })
    except Exception:
        continue

elasticity_df = pd.DataFrame(results)

print(elasticity_df.shape)
print(elasticity_df.groupby('category')['elasticity_score'].mean())
print(elasticity_df.head())

elasticity_df.to_csv('../data/elasticity_scores.csv', index=False)