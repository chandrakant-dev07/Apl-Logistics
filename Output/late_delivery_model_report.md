# APL Logistics Late-Delivery Risk Modeling Report

Generated: 2026-07-08 13:55:30
Input file: `C:\Users\Admin\Downloads\Supply 2 project\apl_logistics_feature_engineered.csv.gz`
Dataset shape: 180,519 rows x 54 columns

## Objective
Build a reproducible baseline model to predict `late_delivery_risk` from the cleaned and engineered order data while avoiding direct delivery-outcome fields removed during cleaning.

## Data Split
- Train rows: 126,363 (late rate 54.83%)
- Validation rows: 27,078 (late rate 54.83%)
- Test rows: 27,078 (late rate 54.83%)
- Majority-class baseline accuracy on test: 0.548

## Feature Preparation
- Numeric and engineered numeric features: 40
- One-hot categorical groups: 11
- Total model features after encoding: 194
- Frequency encoding was fit on the training split only for high-cardinality location/product columns.
- Numeric scaling and categorical level selection were fit on the training split only.

## Training Summary
- Model: L2-regularized logistic regression trained with mini-batch Adam.
- Final train log loss: 0.5219
- Final validation log loss: 0.5198

## Evaluation
| Split / threshold | Accuracy | Precision | Recall | F1 | ROC-AUC | Avg precision | Log loss |
|---|---:|---:|---:|---:|---:|---:|---:|
| Validation @ 0.50 | 0.712 | 0.888 | 0.544 | 0.675 | 0.774 | 0.840 | 0.520 |
| Validation @ 0.30 | 0.598 | 0.578 | 0.983 | 0.728 | 0.774 | 0.840 | 0.520 |
| Test @ 0.50 | 0.711 | 0.886 | 0.542 | 0.672 | 0.771 | 0.837 | 0.522 |
| Test @ 0.30 | 0.599 | 0.579 | 0.982 | 0.729 | 0.771 | 0.837 | 0.522 |

## Top Positive Risk Signals
| feature | coefficient |
| --- | --- |
| cat__order_status__PENDING | 2.8226 |
| cat__order_status__PROCESSING | 2.7534 |
| cat__type__PAYMENT | 0.6800 |
| cat__type__DEBIT | 0.6659 |
| cat__order_status__CLOSED | 0.6002 |
| cat__type__CASH | 0.6002 |
| cat__order_status__PENDING_PAYMENT | 0.5868 |
| cat__order_status__COMPLETE | 0.5372 |
| cat__order_status__ON_HOLD | 0.5151 |
| cat__order_status__PAYMENT_REVIEW | 0.4444 |
| num__first_class_shipping_flag | 0.3836 |
| cat__shipping_mode__First_Class | 0.3482 |

## Top Negative Risk Signals
| feature | coefficient |
| --- | --- |
| cat__order_status__SUSPECTED_FRAUD | -3.0414 |
| cat__order_status__CANCELED | -3.0038 |
| cat__type__TRANSFER | -1.6043 |
| num__scheduled_zero_day_flag | -0.3925 |
| num__same_day_shipping_flag | -0.3925 |
| cat__shipping_mode__Same_Day | -0.3617 |
| cat__order_region__Canada | -0.2969 |
| cat__customer_state__CO | -0.2806 |
| cat__category_name__Baseball_Softball | -0.2449 |
| cat__shipping_mode__Standard_Class | -0.2177 |
| num__standard_class_shipping_flag | -0.1817 |
| num__mode_avg_scheduled_days | -0.1780 |

## Saved Artifacts
- Metrics JSON: `outputs\late_delivery_model\metrics.json`
- Feature coefficients: `outputs\late_delivery_model\feature_importance.csv`
- Model coefficients/config: `outputs\late_delivery_model\model_coefficients.csv`, `outputs\late_delivery_model\model_config.json`
- Score distribution CSV: `outputs\late_delivery_model\score_distribution.csv`
- Score plot skipped; see `outputs\late_delivery_model\score_distribution.error.txt`
- Scored test rows: `outputs\late_delivery_model\scored_test_rows.csv`
- Late-risk segment summary: `outputs\late_delivery_model\late_risk_segment_summary.csv`
- Late-risk view: `outputs\late_delivery_model\late_risk_view.md`

## Recommended Next Step
Use the late-risk view to prioritize operational follow-up, then compare this baseline against a stronger tree-based model after installing `scikit-learn` or another ML package.
