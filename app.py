import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime

# --- CONFIG & THEME ---
st.set_page_config(page_title="Sales Command Center", layout="wide")

# Custom Dark Glassmorphism CSS
st.markdown("""
    <style>
    .main { background: #0b0e14; color: #e0e0e0; }
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border-left: 5px solid #ff4b4b;
        padding: 15px;
        border-radius: 10px;
    }
    .stAlert { background: rgba(255, 75, 75, 0.1); border: none; color: #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA ENGINE ---
@st.cache_data
def generate_complex_data():
    dates = pd.date_range(start="2026-01-01", periods=120, freq='D')
    # Trend: Growing then a sharp dip in the last 30 days
    trend = np.linspace(100, 120, 90).tolist() + np.linspace(120, 70, 30).tolist()
    noise = np.random.normal(0, 5, 120)
    sales = [t + n for t, n in zip(trend, noise)]
    
    df = pd.DataFrame({"Date": dates, "Sales": sales})
    df['Day'] = df['Date'].dt.day_name()
    df['Month'] = df['Date'].dt.month_name()
    return df

df = generate_complex_data()

# --- SIDEBAR: STRATEGY ROOM ---
with st.sidebar:
    st.title("🛡️ Recovery Room")
    st.info("The system has detected a **24% revenue drop** over the last 30 days.")
    
    st.subheader("Intervention Level")
    mode = st.radio("Strategy Mode", ["Passive Observation", "Standard Recovery", "Aggressive Reversal"])
    
    st.subheader("Budget Shift")
    ads = st.slider("Ad Spend Increase (%)", 0, 100, 25)
    discount = st.slider("Flash Discount Rate (%)", 0, 40, 10)

# --- HEADER SECTION ---
col_h1, col_h2 = st.columns([2, 1])
with col_h1:
    st.title("System Status: **Critical Decline** 📉")
    st.write("Real-time sales velocity tracking and churn mitigation.")

with col_h2:
    # A custom 'Pulse' indicator
    pulse_val = 42 if mode == "Passive Observation" else 78
    st.markdown(f"**System Health Pulse:** {'🔴' if pulse_val < 50 else '🟢'} {pulse_val}%")
    st.progress(pulse_val / 100)

# --- ROW 1: THE "LEAK" METRICS ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("Current Velocity", f"${df['Sales'].iloc[-1]:.1f}k", "-18%", delta_color="inverse")
m2.metric("Customer Churn", "12.4%", "2.1%", delta_color="inverse")
m3.metric("Burn Rate", "$4.2k/day", "High", delta_color="off")
m4.metric("Avg. Order Value", "$142", "-$12", delta_color="inverse")

st.divider()

# --- ROW 2: ADVANCED VISUALS ---
left_vis, right_vis = st.columns([1.5, 1])

with left_vis:
    st.subheader("Revenue Trajectory vs. Prediction")
    # Plotting history + a simple projection
    fig_main = go.Figure()
    fig_main.add_trace(go.Scatter(x=df['Date'], y=df['Sales'], name="Actual Sales", line=dict(color='#00d1ff', width=3)))
    
    # Projection Logic
    future_dates = pd.date_range(start=df['Date'].iloc[-1], periods=30, freq='D')
    proj_val = df['Sales'].iloc[-1]
    if mode == "Aggressive Reversal":
        projection = [proj_val * (1 + 0.01)**i for i in range(30)]
        p_color = "#00ff88"
    else:
        projection = [proj_val * (1 - 0.005)**i for i in range(30)]
        p_color = "#ff4b4b"
        
    fig_main.add_trace(go.Scatter(x=future_dates, y=projection, name="AI Projection", line=dict(color=p_color, dash='dot')))
    fig_main.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=20, b=20))
    st.plotly_chart(fig_main, use_container_width=True)

with right_vis:
    st.subheader("Loss Concentration (by Day)")
    # Heatmap to see which days of the week are failing
    day_stats = df.tail(30).groupby('Day')['Sales'].mean().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    fig_heat = px.bar(day_stats, x=day_stats.index, y=day_stats.values, color=day_stats.values, 
                     color_continuous_scale='Reds_r', labels={'y':'Avg Sales'})
    fig_heat.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
    st.plotly_chart(fig_heat, use_container_width=True)

# --- ROW 3: ACTIONABLE INSIGHTS ---
st.subheader("💡 Strategic Anomalies Detected")
c1, c2 = st.columns(2)

with c1:
    st.error("**Anomaly:** Weekend sales in the 'North' region have dropped by **40%** compared to the 90-day average.")
    st.button("Generate Regional Breakdown")

with c2:
    st.warning("**Observation:** Conversion rate is stable, but Traffic Volume is declining. This suggests a top-of-funnel marketing issue.")
    if st.button("Apply Recovery Strategy"):
        st.balloons()
        st.success("Strategy Deployed: Discount codes sent to high-risk churn customers.")

# --- DATA AUDIT ---
with st.expander("📥 Access Raw Sales Audit Log"):
    st.dataframe(df.sort_values(by="Date", ascending=False), use_container_width=True)
