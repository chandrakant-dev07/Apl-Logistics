# APL Logistics — Late Delivery Risk Dashboard

Predicts, before an order ships, the probability that it will be delivered late — with
risk scoring, explainability, and an operations action panel.

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the URL Streamlit prints (usually http://localhost:8501).

## What's inside

- `app.py` — the dashboard (Streamlit)
- `artifacts/model_xgb.joblib` — trained XGBoost classifier (ROC-AUC 0.82, F1 0.75 on held-out test data)
- `artifacts/ohe.joblib`, `artifacts/target_encodings.joblib` — fitted encoders for categorical features
- `artifacts/fe_params.joblib` — feature-engineering parameters (region volume map, congestion tier bins, z-score stats) used to transform new/what-if orders identically to training data
- `artifacts/feature_columns.joblib` — exact column order the model expects
- `artifacts/dashboard_data.parquet` — all 172,762 modeling-eligible orders, pre-scored with risk probability and category

## Dashboard modules

1. **Delay Risk Overview** — total orders, high-risk count, probability distribution
2. **Order-Level Risk Prediction** — look up an existing order's score, or use the
   what-if predictor to score a hypothetical new order in real time (with SHAP-based
   explanation of the top factors driving that specific prediction)
3. **Region & Mode Risk Analysis** — heatmap of risk by region × shipping mode
4. **Operations Action Panel** — orders above your chosen risk threshold, sorted by
   priority, downloadable as CSV

## Filters (sidebar)

Shipping mode, market/region, customer segment, and a risk threshold slider that
drives both the Overview metrics and the Operations Action Panel.

## Important modeling note

`Delivery Status` and `Days for shipping (real)` were excluded from the model —
both are only known *after* an order ships, and using them would leak the answer.
`Order Status` values `CANCELED` and `SUSPECTED_FRAUD` (orders that never actually
ship) were excluded from training entirely, since "late" is undefined for them.
See the accompanying research paper for the full methodology and EDA.
