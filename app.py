import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- PAGE CONFIG ---
st.set_page_config(page_title="Sales Recovery Lab", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- DATA ENGINE ---
@st.cache_data
def get_default_data():
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    return pd.DataFrame({
        "Month": months,
        "Revenue": [12000, 11500, 10800, 9500, 8200, 7500],
        "Leads": [500, 480, 410, 350, 300, 280],
        "Avg_Deal_Size": [24, 23.9, 26.3, 27.1, 27.3, 26.7],
        "Competitor_Activity": [2, 3, 5, 8, 9, 10] # Scale 1-10
    })

# --- SIDEBAR: INTERACTIVE INPUTS ---
st.sidebar.header("🛠️ Simulation Workspace")
uploaded_file = st.sidebar.file_uploader("Upload Sales CSV", type=["csv"])

st.sidebar.subheader("Strategic Levers")
adj_price = st.sidebar.slider("Price Adjustment (%)", -20, 20, 0)
adj_marketing = st.sidebar.slider("Marketing Boost (%)", 0, 100, 10)
target_conversion = st.sidebar.number_input("Target Lead Conversion (%)", value=5.0, step=0.5)

# --- LOAD DATA ---
df = pd.read_csv(uploaded_file) if uploaded_file else get_default_data()

# --- HEADER SECTION ---
st.title("📈 Sales Decline & Recovery Lab")
st.info("Interactive dashboard for root-cause analysis and solution modeling.")

# --- ROW 1: KPI TILES ---
col1, col2, col3, col4 = st.columns(4)
current_rev = df["Revenue"].iloc[-1]
prev_rev = df["Revenue"].iloc[-2]
rev_delta = ((current_rev - prev_rev) / prev_rev) * 100

col1.metric("Current Revenue", f"${current_rev:,}", f"{rev_delta:.1f}%")
col2.metric("Lead Volume", df["Leads"].iloc[-1], "-12% vs LY")
col3.metric("Competitor Pressure", f"{df['Competitor_Activity'].iloc[-1]}/10", "+40% Increase", delta_color="inverse")
col4.metric("Market Sentiment", "Neutral", "📉 Dropping")

st.divider()

# --- ROW 2: INTERACTIVE CHARTS ---
tab1, tab2 = st.tabs(["📊 Diagnostic View", "🧪 Strategy Simulator"])

with tab1:
    c1, c2 = st.columns([2, 1])
    
    with c1:
        # Multi-axis chart
        fig = px.line(df, x="Month", y=["Revenue", "Leads"], 
                     title="Revenue vs. Lead Generation Decay",
                     color_discrete_sequence=["#1f77b4", "#ff7f0e"], markers=True)
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        st.subheader("Loss Attribution")
        attr_data = pd.DataFrame({
            "Reason": ["Pricing", "Competitors", "Product Fit", "Marketing"],
            "Weight": [35, 40, 10, 15]
        })
        fig_pie = px.pie(attr_data, values='Weight', names='Reason', hole=.4,
                         color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_pie, use_container_width=True)

with tab2:
    st.subheader("Predictive Recovery Model")
    st.write("Adjust the sliders in the sidebar to see the projected impact on revenue.")
    
    # Simple Math Model: New Revenue = Base + (Marketing Effect) - (Price Elasticity)
    base_rev = current_rev
    marketing_impact = (adj_marketing * 0.05) * base_rev / 100
    price_impact = (adj_price * -1.5) * base_rev / 100 # Assuming 1.5 price elasticity
    
    projected_rev = base_rev + marketing_impact + price_impact
    
    # Comparison Chart
    comparison_df = pd.DataFrame({
        "Scenario": ["Current (Actual)", "Projected (Simulated)"],
        "Revenue": [base_rev, projected_rev]
    })
    
    fig_sim = px.bar(comparison_df, x="Scenario", y="Revenue", 
                    color="Scenario", text_auto='.2s',
                    color_discrete_map={"Current (Actual)": "#7f8c8d", "Projected (Simulated)": "#27ae60"})
    st.plotly_chart(fig_sim, use_container_width=True)
    
    if projected_rev > base_rev:
        st.success(f"✅ Strategy Result: Expected Gain of **${(projected_rev - base_rev):,.2f}** next month.")
    else:
        st.error(f"⚠️ Strategy Result: Potential further loss of **${(base_rev - projected_rev):,.2f}**.")

# --- ROW 3: DYNAMIC RECOMMENDATIONS ---
st.divider()
st.subheader("📋 AI-Generated Action Plan")

# Logic-based recommendations
recs = []
if df["Competitor_Activity"].iloc[-1] > 7:
    recs.append("**Aggressive Retention:** Launch a loyalty discount to counter competitor poaching.")
if adj_marketing < 20:
    recs.append("**Visibility Gap:** Increase top-of-funnel spend by at least 25% to stabilize lead flow.")
if adj_price > 5:
    recs.append("**Margin Risk:** High price increases may accelerate churn. Consider 'Value Bundling' instead.")

for r in recs:
    st.markdown(f"- {r}")

# --- DOWNLOAD REPORT ---
st.sidebar.divider()
st.sidebar.download_button("Export Analysis (CSV)", df.to_csv(), "sales_analysis.csv")
