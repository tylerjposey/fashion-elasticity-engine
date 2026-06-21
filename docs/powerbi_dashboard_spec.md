# Power BI Dashboard Specification

## Dashboard Purpose

The Power BI dashboard turns the Fashion Elasticity Engine into a client-facing markdown decision tool. It is designed for retail category managers, pricing analysts, and technology consulting stakeholders who need to decide which apparel SKUs should be marked down, how deep the markdown should be, and what projected revenue impact the markdown may create.

The central business question is:

> Which products should be marked down, by how much, and what revenue impact should the business expect?

## Intended Audience

| Audience | Primary Question |
|---|---|
| Executive stakeholder | How large is the markdown opportunity? |
| Category manager | Which SKUs need action first? |
| Pricing analyst | How sensitive are products to price changes? |
| Technology consultant | How does the pipeline support repeatable decision-making? |

## Recommended Data Model

```text
dim_products
    sku_id
    category

fact_weekly_sales
    week_id
    sku_id
    price
    units_sold
    sales_velocity
    inventory_age_days

fact_markdown_recommendations
    sku_id
    elasticity_score
    current_price
    recommended_price
    discount_pct
    projected_units_sold
    projected_revenue
    projected_margin_lift_pct
    urgency_flag
```

## Recommended Relationships

| From Table | From Field | To Table | To Field | Cardinality |
|---|---|---|---|---|
| dim_products | sku_id | fact_weekly_sales | sku_id | One-to-many |
| dim_products | sku_id | fact_markdown_recommendations | sku_id | One-to-many |

Use single-direction filtering from `dim_products` to the fact tables unless a specific visual requires otherwise.

## Dashboard Pages

## Page 1: Executive Markdown Overview

### Objective

Provide a high-level view of markdown exposure, projected revenue, and urgency mix.

### Recommended Visuals

| Visual | Fields / Measure | Purpose |
|---|---|---|
| KPI card | Total Projected Revenue | Shows total expected revenue under recommendations |
| KPI card | Average Recommended Discount | Communicates average markdown depth |
| KPI card | Immediate SKU Count | Shows number of urgent products |
| KPI card | Average Projected Revenue Lift % | Shows average modeled upside |
| Bar chart | Projected revenue by category | Identifies highest-value categories |
| Donut chart | SKU count by urgency flag | Summarizes action mix |
| Table | Top 10 markdown opportunities | Provides immediate executive action list |

### Recommended Slicers

- Category
- Urgency flag
- Discount percentage range
- Elasticity score range

## Page 2: SKU Prioritization

### Objective

Help a category manager decide which SKUs to act on first.

### Recommended Visuals

| Visual | Fields / Measure | Purpose |
|---|---|---|
| Matrix/table | SKU, category, current price, recommended price, discount %, projected revenue, urgency flag | Main action list |
| Conditional formatting | urgency_flag | Highlights IMMEDIATE, MONITOR, HOLD |
| Scatter plot | elasticity_score vs projected revenue lift % | Identifies responsive/high-impact SKUs |
| Bar chart | Top SKUs by projected revenue | Ranks revenue opportunities |
| Bar chart | Top SKUs by discount percentage | Highlights deepest markdown recommendations |

### Recommended Sort Logic

Sort SKU tables by:

1. `urgency_flag`, with IMMEDIATE first
2. `projected_revenue` descending
3. `discount_pct` descending

## Page 3: Elasticity & Price Sensitivity

### Objective

Show model behavior and explain how price sensitivity differs by category and SKU.

### Recommended Visuals

| Visual | Fields / Measure | Purpose |
|---|---|---|
| Bar chart | Average elasticity by category | Compares category-level price sensitivity |
| Histogram | elasticity_score | Shows distribution of SKU elasticity |
| Scatter plot | current_price vs projected_units_sold | Shows price-volume relationship |
| Table | SKU, category, elasticity_score, discount_pct, projected_units_sold | Supports model inspection |

### Interpretation Notes

- More negative elasticity values indicate stronger modeled price sensitivity.
- Elasticity estimates are based on simulated weekly price history and should be treated as prototype decision-support outputs.
- The dashboard should avoid claiming causal lift unless real markdown experiment data is added later.

## Page 4: Markdown Scenario Analysis

### Objective

Allow stakeholders to test how different discount levels may affect projected units and revenue.

### Optional Power BI Feature

Create a What-if Parameter:

| Parameter | Suggested Range |
|---|---|
| Selected Discount % | 0% to 50%, increment 1% |

### Recommended Visuals

| Visual | Fields / Measure | Purpose |
|---|---|---|
| What-if slicer | Selected Discount % | Lets user simulate markdown depth |
| Line chart | Projected revenue by selected discount | Shows scenario curve |
| Card | Scenario projected revenue | Shows selected scenario output |
| Card | Scenario projected units | Shows selected scenario volume |
| Table | Recommended discount vs selected discount | Compares model recommendation to manual scenario |

## Recommended DAX Measures

```DAX
Total Projected Revenue =
SUM(fact_markdown_recommendations[projected_revenue])
```

```DAX
Average Recommended Discount =
AVERAGE(fact_markdown_recommendations[discount_pct])
```

```DAX
Immediate SKU Count =
CALCULATE(
    DISTINCTCOUNT(fact_markdown_recommendations[sku_id]),
    fact_markdown_recommendations[urgency_flag] = "IMMEDIATE"
)
```

```DAX
Monitor SKU Count =
CALCULATE(
    DISTINCTCOUNT(fact_markdown_recommendations[sku_id]),
    fact_markdown_recommendations[urgency_flag] = "MONITOR"
)
```

```DAX
Hold SKU Count =
CALCULATE(
    DISTINCTCOUNT(fact_markdown_recommendations[sku_id]),
    fact_markdown_recommendations[urgency_flag] = "HOLD"
)
```

```DAX
Average Elasticity =
AVERAGE(fact_markdown_recommendations[elasticity_score])
```

```DAX
Average Projected Revenue Lift % =
AVERAGE(fact_markdown_recommendations[projected_margin_lift_pct])
```

```DAX
Average Recommended Price =
AVERAGE(fact_markdown_recommendations[recommended_price])
```

```DAX
SKU Count =
DISTINCTCOUNT(fact_markdown_recommendations[sku_id])
```

## Recommended Conditional Formatting

| Field | Rule |
|---|---|
| urgency_flag = IMMEDIATE | Red background or high-priority icon |
| urgency_flag = MONITOR | Yellow/orange background or medium-priority icon |
| urgency_flag = HOLD | Green/neutral background or low-priority icon |
| discount_pct > 30 | Highlight as deep markdown |
| projected_margin_lift_pct > 0 | Positive indicator |

## Recommended Dashboard Layout

### Executive Page Layout

```text
[KPI: Revenue] [KPI: Avg Discount] [KPI: Immediate SKUs] [KPI: Avg Lift]

[Projected Revenue by Category]      [Urgency Mix Donut]

[Top 10 Markdown Opportunities Table]
```

### SKU Prioritization Layout

```text
[Slicers: Category | Urgency | Discount Range]

[SKU Action Table]

[Elasticity vs Revenue Lift Scatter]

[Top SKUs by Projected Revenue]
```

## Portfolio Presentation Notes

When presenting this dashboard, describe it as a decision-support layer, not an automated pricing system.

Suggested explanation:

> I built a markdown decision-support dashboard that helps retail stakeholders prioritize slow-moving apparel SKUs, evaluate recommended discount levels, and estimate projected revenue impact. The dashboard connects Python-generated elasticity and optimization outputs to a Power BI reporting layer designed for executive and category-manager decisioning.

## Future Dashboard Enhancements

- Add gross margin and cost-of-goods data.
- Add inventory-on-hand and sell-through percentage.
- Add lifecycle stage: launch, growth, maturity, clearance.
- Add seasonality filters.
- Add Power BI bookmarks for executive vs analyst views.
- Export dashboard screenshots for the GitHub README and portfolio website.
