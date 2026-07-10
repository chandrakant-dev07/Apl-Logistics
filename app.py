"""
APL Logistics — Late Delivery Risk Dashboard
Run with: streamlit run app.py
"""
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
import shap
import os

st.set_page_config(page_title="APL Logistics — Late Delivery Risk", layout="wide")

ART = os.path.join(os.path.dirname(__file__), "artifacts")
_REQUIRED = ["dashboard_data.parquet", "model_xgb.joblib", "ohe.joblib",
             "target_encodings.joblib", "feature_columns.joblib", "fe_params.joblib"]

if not all(os.path.exists(os.path.join(ART, f)) for f in _REQUIRED):
    # Common cause: files were uploaded individually via the GitHub website,
    # which drops the "artifacts/" folder structure and lands everything in
    # the repo root instead. Fall back to looking next to app.py.
    _fallback = os.path.dirname(__file__)
    if all(os.path.exists(os.path.join(_fallback, f)) for f in _REQUIRED):
        ART = _fallback
    else:
        _base = os.path.dirname(__file__)
        _found = os.listdir(_base) if os.path.isdir(_base) else []
        _found_art = os.listdir(ART) if os.path.isdir(ART) else []
        st.error(
            "Missing required data files. The dashboard needs these 6 files either in an "
            "`artifacts/` subfolder next to app.py, or directly next to app.py:\n\n"
            + "\n".join(f"- {f}" for f in _REQUIRED)
            + f"\n\nFiles found next to app.py: {_found or 'none'}"
            + f"\nFiles found in artifacts/: {_found_art or 'folder not found'}"
            + "\n\nIf you uploaded files individually via the GitHub website, they likely "
              "landed in the repo root without the `artifacts/` folder. Either move them into "
              "an `artifacts` folder (rename each file to `artifacts/<filename>` using GitHub's "
              "rename/edit feature), or leave them in the root — this app will find them either way."
        )
        st.stop()


# ---------------------------------------------------------------------------
# Load data & model artifacts (cached)
# ---------------------------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_parquet(os.path.join(ART, "dashboard_data.parquet"))


@st.cache_resource
def load_model_artifacts():
    model = joblib.load(os.path.join(ART, "model_xgb.joblib"))
    ohe = joblib.load(os.path.join(ART, "ohe.joblib"))
    encodings = joblib.load(os.path.join(ART, "target_encodings.joblib"))
    feature_cols = joblib.load(os.path.join(ART, "feature_columns.joblib"))
    fe_params = joblib.load(os.path.join(ART, "fe_params.joblib"))
    explainer = shap.TreeExplainer(model)
    return model, ohe, encodings, feature_cols, fe_params, explainer


df = load_data()
model, ohe, encodings, feature_cols, fe_params, explainer = load_model_artifacts()

LOW_CARD_CAT = ['Type', 'Customer Segment', 'Customer Country', 'Department Name',
                'Market', 'Order Region', 'Order Status', 'Shipping Mode',
                'region_congestion_tier']
HIGH_CARD_CAT = ['Category Name', 'Customer City', 'Customer State',
                  'Order City', 'Order Country', 'Order State', 'Product Name']
GLOBAL_MEAN = df['Late_delivery_risk'].mean()


def congestion_tier_for_volume(v, edges):
    if v <= edges[1]:
        return 'Low'
    elif v <= edges[2]:
        return 'Medium'
    else:
        return 'High'


def build_feature_row(raw: dict) -> pd.DataFrame:
    """Take a dict of raw order attributes and produce the fully engineered,
    encoded single-row feature matrix the model expects."""
    row = dict(raw)

    row['is_express_shipping'] = 1 if row['Days for shipment (scheduled)'] <= 2 else 0
    row['shipping_pressure_index'] = row['Order Item Quantity'] / (row['Days for shipment (scheduled)'] + 1)
    vol = fe_params['region_volume_map'].get(row['Order Region'], fe_params['region_volume_default'])
    row['region_order_volume'] = vol
    row['region_congestion_tier'] = congestion_tier_for_volume(vol, fe_params['congestion_bin_edges'])
    row['order_complexity_score'] = (
        (row['Order Item Quantity'] - fe_params['quantity_mean']) / fe_params['quantity_std']
        + (row['Order Item Discount Rate'] - fe_params['discount_rate_mean']) / fe_params['discount_rate_std']
        + (row['Product Price'] - fe_params['price_mean']) / fe_params['price_std']
    )

    r = pd.DataFrame([row])

    for col in HIGH_CARD_CAT:
        r[col + '_te'] = r[col].map(encodings[col]).fillna(GLOBAL_MEAN)
    r = r.drop(columns=HIGH_CARD_CAT)

    ohe_arr = ohe.transform(r[LOW_CARD_CAT])
    ohe_df = pd.DataFrame(ohe_arr, columns=ohe.get_feature_names_out(LOW_CARD_CAT), index=r.index)
    r_final = pd.concat([r.drop(columns=LOW_CARD_CAT), ohe_df], axis=1)
    r_final = r_final.reindex(columns=feature_cols, fill_value=0)
    return r_final


# ---------------------------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------------------------
st.sidebar.title("APL Logistics")
st.sidebar.caption("Late Delivery Risk Dashboard")

shipping_modes = st.sidebar.multiselect(
    "Shipping mode", sorted(df['Shipping Mode'].unique()), default=sorted(df['Shipping Mode'].unique())
)
markets = st.sidebar.multiselect(
    "Market / region", sorted(df['Market'].unique()), default=sorted(df['Market'].unique())
)
segments = st.sidebar.multiselect(
    "Customer segment", sorted(df['Customer Segment'].unique()), default=sorted(df['Customer Segment'].unique())
)
risk_threshold = st.sidebar.slider("Risk threshold (flag as high-risk above)", 0.0, 1.0, 0.65, 0.01)

fdf = df[
    df['Shipping Mode'].isin(shipping_modes)
    & df['Market'].isin(markets)
    & df['Customer Segment'].isin(segments)
].copy()

st.sidebar.markdown("---")
st.sidebar.metric("Orders matching filters", f"{len(fdf):,}")

tab1, tab2, tab3, tab4 = st.tabs([
    "Delay Risk Overview", "Order-Level Prediction", "Region & Mode Analysis", "Operations Action Panel"
])

# ---------------------------------------------------------------------------
# TAB 1 — Delay Risk Overview
# ---------------------------------------------------------------------------
with tab1:
    st.subheader("Delay risk overview")

    high_risk_n = (fdf['late_probability'] >= risk_threshold).sum()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total orders", f"{len(fdf):,}")
    c2.metric("High-risk orders", f"{high_risk_n:,}", f"{high_risk_n / max(len(fdf),1):.1%}")
    c3.metric("Avg. late probability", f"{fdf['late_probability'].mean():.1%}")
    c4.metric("Actual late rate", f"{fdf['Late_delivery_risk'].mean():.1%}")

    col1, col2 = st.columns(2)
    with col1:
        fig = px.histogram(fdf, x='late_probability', nbins=40,
                            title="Distribution of predicted late-delivery probability")
        fig.add_vline(x=risk_threshold, line_dash="dash", line_color="red")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        cat_counts = fdf['risk_category'].value_counts().reindex(['Low Risk', 'Medium Risk', 'High Risk'])
        fig2 = px.bar(cat_counts, title="Orders by risk category",
                       color=cat_counts.index,
                       color_discrete_map={'Low Risk': '#1baf7a', 'Medium Risk': '#eda100', 'High Risk': '#e34948'})
        fig2.update_layout(showlegend=False, xaxis_title="", yaxis_title="Orders")
        st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------------------------------
# TAB 2 — Order-Level Risk Prediction
# ---------------------------------------------------------------------------
with tab2:
    st.subheader("Order-level risk prediction")
    mode = st.radio("Mode", ["Look up an existing order", "What-if predictor (new order)"], horizontal=True)

    if mode == "Look up an existing order":
        order_id = st.number_input("Order ID", min_value=int(fdf['Order_Id'].min()) if len(fdf) else 1,
                                    max_value=int(fdf['Order_Id'].max()) if len(fdf) else 1, value=int(fdf['Order_Id'].iloc[0]) if len(fdf) else 1)
        match = fdf[fdf['Order_Id'] == order_id]
        if match.empty:
            st.warning("Order ID not found in current filtered set.")
        else:
            row = match.iloc[0]
            c1, c2, c3 = st.columns(3)
            c1.metric("Late probability", f"{row['late_probability']:.1%}")
            c2.metric("Risk category", row['risk_category'])
            c3.metric("Actually late?", "Yes" if row['Late_delivery_risk'] == 1 else "No")
            detail_cols = ['Shipping Mode', 'Days for shipment (scheduled)', 'Order Region', 'Market',
                           'Customer Segment', 'Category Name', 'Product Price', 'Order Item Quantity']
            st.dataframe(match[detail_cols], use_container_width=True, hide_index=True)

    else:
        st.caption("Fill in order attributes to get a live risk prediction before the order ships.")
        c1, c2, c3 = st.columns(3)
        with c1:
            shipping_mode = st.selectbox("Shipping mode", sorted(df['Shipping Mode'].unique()))
            days_map = {'Same Day': 0, 'First Class': 1, 'Second Class': 2, 'Standard Class': 4}
            scheduled_days = days_map[shipping_mode]
            st.caption(f"Scheduled shipping days: {scheduled_days}")
            order_region = st.selectbox("Order region", sorted(df['Order Region'].unique()))
            market = st.selectbox("Market", sorted(df['Market'].unique()))
        with c2:
            category = st.selectbox("Category", sorted(df['Category Name'].unique()))
            segment = st.selectbox("Customer segment", sorted(df['Customer Segment'].unique()))
            order_status = st.selectbox("Order status", sorted(df['Order Status'].unique()))
        with c3:
            quantity = st.slider("Order item quantity", 1, 5, 2)
            price = st.number_input("Product price ($)", min_value=9.99, max_value=1999.99, value=100.0)
            discount_rate = st.slider("Discount rate", 0.0, 0.25, 0.10, 0.01)

        if st.button("Predict risk", type="primary"):
            raw = {
                'Type': 'DEBIT',
                'Days for shipment (scheduled)': scheduled_days,
                'Category Name': category,
                'Customer City': df['Customer City'].mode()[0],
                'Customer Country': df['Customer Country'].mode()[0],
                'Customer Segment': segment,
                'Customer State': df['Customer State'].mode()[0],
                'Department Name': df['Department Name'].mode()[0],
                'Market': market,
                'Order City': df['Order City'].mode()[0],
                'Order Country': df['Order Country'].mode()[0],
                'Order Item Discount': price * discount_rate,
                'Order Item Discount Rate': discount_rate,
                'Order Item Profit Ratio': 0.12,
                'Order Item Quantity': quantity,
                'Sales': price * quantity,
                'Order Item Total': price * quantity * (1 - discount_rate),
                'Order Profit Per Order': price * quantity * 0.12,
                'Order Region': order_region,
                'Order State': df['Order State'].mode()[0],
                'Order Status': order_status,
                'Product Name': df['Product Name'].mode()[0],
                'Product Price': price,
                'Shipping Mode': shipping_mode,
                'Latitude': df['Latitude'].median(),
                'Longitude': df['Longitude'].median(),
            }
            X_row = build_feature_row(raw)
            proba = model.predict_proba(X_row)[0, 1]
            cat = 'Low Risk' if proba < 0.35 else ('Medium Risk' if proba < 0.65 else 'High Risk')

            c1, c2 = st.columns(2)
            c1.metric("Predicted late probability", f"{proba:.1%}")
            c2.metric("Risk category", cat)

            shap_vals = explainer.shap_values(X_row)[0]
            contrib = pd.DataFrame({'feature': X_row.columns, 'shap': shap_vals})
            contrib['abs'] = contrib['shap'].abs()
            top = contrib.sort_values('abs', ascending=False).head(8)
            fig = go.Figure(go.Bar(
                x=top['shap'], y=top['feature'], orientation='h',
                marker_color=['#e34948' if v > 0 else '#1baf7a' for v in top['shap']]
            ))
            fig.update_layout(title="Top factors driving this prediction (red = raises risk, green = lowers it)",
                               xaxis_title="SHAP value", yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# TAB 3 — Region & Mode Risk Analysis
# ---------------------------------------------------------------------------
with tab3:
    st.subheader("Region & shipping mode risk analysis")

    pivot = fdf.pivot_table(values='late_probability', index='Order Region', columns='Shipping Mode', aggfunc='mean')
    fig = px.imshow(pivot, color_continuous_scale='Reds', aspect='auto',
                     title="Avg. predicted late probability by region and shipping mode")
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

    mode_risk = fdf.groupby('Shipping Mode')['late_probability'].mean().sort_values(ascending=False)
    fig2 = px.bar(mode_risk, title="Avg. late probability by shipping mode", labels={'value': 'Avg. late probability'})
    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------------------------------
# TAB 4 — Operations Action Panel
# ---------------------------------------------------------------------------
with tab4:
    st.subheader("Operations action panel")
    st.caption(f"Orders at or above the risk threshold ({risk_threshold:.0%}), sorted by priority.")

    action_df = fdf[fdf['late_probability'] >= risk_threshold].sort_values('late_probability', ascending=False)
    st.metric("Orders requiring attention", f"{len(action_df):,}")

    display_cols = ['Order_Id', 'late_probability', 'risk_category', 'Shipping Mode',
                     'Order Region', 'Market', 'Customer Segment', 'Category Name',
                     'Product Price', 'Order Item Quantity']
    st.dataframe(action_df[display_cols].head(500), use_container_width=True, height=500)

    csv = action_df[display_cols].to_csv(index=False).encode('utf-8')
    st.download_button("Download full action list (CSV)", csv, "high_risk_orders.csv", "text/csv")
