# APL Logistics Late-Risk View

Generated: 2026-07-08 13:55:30
Scope: held-out test split only.

## Executive Summary
- Test orders scored: 27,078
- Actual late rate: 54.8%
- Average predicted late risk: 50.8%
- Intervention threshold: 0.305
- Orders flagged for intervention: 25,157 (92.9%)
- Actual late rate among flagged orders: 57.9%
- High-score orders (score >= 0.700): 9,051 (33.4%)
- Actual late rate among high-score orders: 88.7%

## Highest Predicted-Risk Segments
| segment | segment_value | orders | avg_predicted_risk | actual_late_rate | intervention_rate | high_score_rate |
| --- | --- | --- | --- | --- | --- | --- |
| shipping_mode | First Class | 4180 | 0.9494 | 0.9519 | 0.9519 | 0.9519 |
| shipping_mode | Second Class | 5315 | 0.7298 | 0.7644 | 0.9582 | 0.9543 |
| order_country | Angola | 54 | 0.6202 | 0.5741 | 1.0000 | 0.5000 |
| order_state | Andalucía | 78 | 0.6028 | 0.6538 | 0.9103 | 0.5000 |
| order_state | Sicilia | 65 | 0.5968 | 0.5846 | 0.9692 | 0.4462 |
| order_state | Rajastán | 53 | 0.5961 | 0.5660 | 0.9623 | 0.5094 |
| order_country | Perú | 123 | 0.5860 | 0.5691 | 0.9593 | 0.4634 |
| order_country | Bangladés | 64 | 0.5841 | 0.5625 | 0.9219 | 0.4844 |
| order_state | Lima (ciudad) | 75 | 0.5782 | 0.5467 | 0.9733 | 0.4267 |
| order_state | Massachusetts | 55 | 0.5723 | 0.6727 | 0.9818 | 0.4000 |
| order_state | Estocolmo | 106 | 0.5697 | 0.6321 | 0.9717 | 0.4245 |
| order_state | Baden-Wurtemberg | 120 | 0.5695 | 0.6750 | 0.9750 | 0.4417 |
| customer_state | TN | 248 | 0.5691 | 0.5726 | 0.9637 | 0.3831 |
| order_country | Polonia | 91 | 0.5657 | 0.5385 | 0.9890 | 0.4176 |
| order_state | Gran Casablanca | 54 | 0.5608 | 0.6296 | 0.9630 | 0.4444 |

## Order Status
| segment_value | orders | avg_predicted_risk | actual_late_rate | intervention_rate | actual_late_rate_lift_vs_test |
| --- | --- | --- | --- | --- | --- |
| PAYMENT_REVIEW | 288 | 0.5461 | 0.6215 | 0.9201 | 1.1335 |
| PENDING_PAYMENT | 5957 | 0.5376 | 0.5714 | 0.9916 | 1.0422 |
| COMPLETE | 8924 | 0.5326 | 0.5780 | 0.9729 | 1.0541 |
| CLOSED | 2919 | 0.5282 | 0.5773 | 0.9640 | 1.0528 |
| PENDING | 3124 | 0.5240 | 0.5653 | 0.9786 | 1.0310 |
| PROCESSING | 3276 | 0.5159 | 0.5702 | 0.9362 | 1.0399 |
| ON_HOLD | 1413 | 0.5140 | 0.5570 | 0.9660 | 1.0158 |
| CANCELED | 577 | 0.0384 | 0.0000 | 0.0000 | 0.0000 |

## Shipping Mode
| segment_value | orders | avg_predicted_risk | actual_late_rate | intervention_rate | actual_late_rate_lift_vs_test |
| --- | --- | --- | --- | --- | --- |
| First Class | 4180 | 0.9494 | 0.9519 | 0.9519 | 1.7361 |
| Second Class | 5315 | 0.7298 | 0.7644 | 0.9582 | 1.3942 |
| Same Day | 1432 | 0.3979 | 0.4658 | 0.9574 | 0.8495 |
| Standard Class | 16151 | 0.3302 | 0.3800 | 0.9110 | 0.6931 |

## Market
| segment_value | orders | avg_predicted_risk | actual_late_rate | intervention_rate | actual_late_rate_lift_vs_test |
| --- | --- | --- | --- | --- | --- |
| USCA | 3864 | 0.5172 | 0.5556 | 0.9211 | 1.0134 |
| Europe | 7558 | 0.5159 | 0.5573 | 0.9409 | 1.0164 |
| Pacific Asia | 6200 | 0.5108 | 0.5432 | 0.9500 | 0.9907 |
| Africa | 1799 | 0.5065 | 0.5403 | 0.9327 | 0.9854 |
| LATAM | 7657 | 0.4929 | 0.5417 | 0.9036 | 0.9880 |

## Order Region
| segment_value | orders | avg_predicted_risk | actual_late_rate | intervention_rate | actual_late_rate_lift_vs_test |
| --- | --- | --- | --- | --- | --- |
| Central Asia | 74 | 0.5436 | 0.5946 | 0.9730 | 1.0844 |
| South Asia | 1191 | 0.5333 | 0.5617 | 0.9555 | 1.0245 |
| US Center | 860 | 0.5327 | 0.5558 | 0.9349 | 1.0137 |
| East of USA | 1024 | 0.5308 | 0.5801 | 0.9570 | 1.0579 |
| South of USA | 605 | 0.5281 | 0.5884 | 0.9438 | 1.0732 |
| Central Africa | 241 | 0.5235 | 0.5519 | 0.9544 | 1.0065 |
| Western Europe | 4045 | 0.5191 | 0.5602 | 0.9429 | 1.0217 |
| East Africa | 306 | 0.5169 | 0.5588 | 0.9739 | 1.0192 |

## Category Name
| segment_value | orders | avg_predicted_risk | actual_late_rate | intervention_rate | actual_late_rate_lift_vs_test |
| --- | --- | --- | --- | --- | --- |
| Music | 68 | 0.5567 | 0.6324 | 0.9412 | 1.1533 |
| Baseball & Softball | 98 | 0.5373 | 0.6327 | 0.6122 | 1.1538 |
| Lacrosse | 54 | 0.5334 | 0.6667 | 0.8889 | 1.2159 |
| Cameras | 99 | 0.5313 | 0.5556 | 0.8384 | 1.0132 |
| Pet Supplies | 74 | 0.5265 | 0.5946 | 0.9730 | 1.0844 |
| Women's Clothing | 115 | 0.5187 | 0.5565 | 0.9652 | 1.0150 |
| Accessories | 263 | 0.5173 | 0.5589 | 0.9354 | 1.0194 |
| Boxing & MMA | 72 | 0.5168 | 0.6806 | 0.9167 | 1.2412 |

## Recommended Actions
- Use `intervention_flag` to prioritize orders for proactive shipment review.
- Treat `intervention_flag` as a broad watchlist; it is optimized for recall, not queue size.
- Treat `risk_band = high` as the narrowest queue for urgent operations follow-up.
- Compare this view against a stronger tree-based model before making automated decisions.

## Saved Artifacts
- Scored test rows: `outputs\late_delivery_model\scored_test_rows.csv`
- Segment summary: `outputs\late_delivery_model\late_risk_segment_summary.csv`
