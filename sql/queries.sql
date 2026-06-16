-- 1. Top 20 SKUs by urgency and elasticity score
SELECT r.sku_id, p.category, r.urgency_flag, r.elasticity_score,
       r.recommended_price, r.projected_margin_lift_pct
FROM fact_markdown_recommendations r
JOIN dim_products p ON r.sku_id = p.sku_id
WHERE r.urgency_flag IN ('IMMEDIATE', 'MONITOR')
ORDER BY r.urgency_flag ASC, r.elasticity_score ASC
LIMIT 20;

-- 2. Category-level average elasticity
SELECT p.category, ROUND(AVG(r.elasticity_score)::numeric, 4) AS avg_elasticity
FROM fact_markdown_recommendations r
JOIN dim_products p ON r.sku_id = p.sku_id
GROUP BY p.category
ORDER BY avg_elasticity ASC;

-- 3. Revenue recovery projection by category
SELECT p.category,
       ROUND(SUM(r.projected_revenue)::numeric, 2) AS total_projected_revenue,
       ROUND(AVG(r.projected_margin_lift_pct)::numeric, 2) AS avg_margin_lift_pct
FROM fact_markdown_recommendations r
JOIN dim_products p ON r.sku_id = p.sku_id
GROUP BY p.category
ORDER BY total_projected_revenue DESC;

-- 4. Red flag SKU list (aging > 60 days, velocity below median)
SELECT s.sku_id, p.category, s.inventory_age_days,
       s.sales_velocity, r.urgency_flag, r.projected_margin_lift_pct
FROM fact_weekly_sales s
JOIN dim_products p ON s.sku_id = p.sku_id
JOIN fact_markdown_recommendations r ON s.sku_id = r.sku_id
WHERE s.inventory_age_days > 60
  AND r.urgency_flag = 'IMMEDIATE'
GROUP BY s.sku_id, p.category, s.inventory_age_days,
         s.sales_velocity, r.urgency_flag, r.projected_margin_lift_pct
ORDER BY s.inventory_age_days DESC
LIMIT 20;