import pandas as pd

recommendations = pd.read_csv('../data/markdown_recommendations.csv')
elasticity = pd.read_csv('../data/elasticity_scores.csv')
velocity = pd.read_csv('../data/processed_velocity.csv')

assert not recommendations.empty, 'Recommendations file is empty'
assert not elasticity.empty, 'Elasticity file is empty'
assert not velocity.empty, 'Velocity file is empty'

assert recommendations['discount_pct'].between(5, 40).all(), 'Discount values outside expected range'
assert recommendations['recommended_price'].gt(0).all(), 'Recommended prices must be positive'
assert elasticity['r_squared'].between(0, 1).all(), 'Invalid R-squared values detected'
assert velocity['sales_velocity'].ge(0).all(), 'Negative sales velocity detected'

print('Validation checks passed successfully.')