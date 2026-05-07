import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- PAGE CONFIG ---
st.set_page_config(page_title="Sales Recovery Pro", layout="wide")

# --- ADVANCED CSS (Glassmorphism & Cards) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(160deg, #0f172a 0%, #1e293b 100%); color: #f8fafc; }
    [data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 15px; border-radius: 12px;
    }
    .status-card {
        background: rgba(59, 130, 246, 0.1);
        border-left: 5px solid #3b82f6;
        padding: 20px; border-radius: 10px; margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA SET ---
@st.cache_data
def get_data():
    return pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Revenue": [12500, 11800, 10200, 9100, 8400, 7200],
        "Leads": [450, 430, 310, 240, 210, 190], # Dropping faster than revenue
        "Churn": [2.1, 2.4, 3.1, 4.2, 5.8, 7.2]
    })

df = get_data()

# --- SIDEBAR ---
with st.sidebar:
    st.title("🚀 Simulation")
    price_adj = st.slider("Price Adjustment (%)", -20, 20, -5)
    mkt_boost = st.slider("Marketing Boost (%)", 0, 100, 25)
    st.info("The simulation uses a 1.5x Elasticity model for pricing and 0.8x for marketing reach.")

# --- DYNAMIC EXECUTIVE SUMMARY ---
st.title("📉 Sales Decline Diagnostic")

total_rev_drop = ((df["Revenue"].iloc[-1] - df["Revenue"].iloc[0]) / df["Revenue"].iloc[0]) * 100
lead_drop = ((df["Leads"].iloc[-1] - df["Leads"].iloc[0]) / df["Leads"].iloc[0]) * 100

st.markdown(f"""
<div class="status-card">
    <h4>Executive Summary</h4>
    Revenue has declined by <b>{total_rev_drop:.1f}%</b> since January. 
    Crucially, <b>Leads have dropped by {lead_drop:.1f}%</b>, suggesting the revenue slide will 
    accelerate in July unless marketing volume is restored.
</div>
""", unsafe_allow_html=True)

# --- TOP METRICS ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Overall Decline", f"{total_rev_drop:.1f}%", "-4.2% MoM")
c2.metric("Market Share Loss", "-11.5%", "Critical", delta_color="inverse")
c3.metric("Churn Rate", f"{df['Churn'].iloc[-1]}%", "+1.2%", delta_color="inverse")
c4.metric("Lead Quality Score", "64/100", "-12 pts")

st.divider()

# --- MAIN TABS ---
tab1, tab2 = st.tabs(["📊 Diagnostic View", "🧪 Strategy Simulator"])

with tab1:
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        # DUAL AXIS CHART: REVENUE VS LEADS
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(go.Bar(x=df["Month"], y=df["Revenue"], name="Revenue ($)", 
                             marker_color='rgba(59, 130, 246, 0.6)'), secondary_y=False)
        
        fig.add_trace(go.Scatter(x=df["Month"], y=df["Leads"], name="Lead Volume", 
                                 line=dict(color='#fbbf24', width=4)), secondary_y=True)
        
        fig.update_layout(title="Revenue vs. Lead Generation Decay (Correlation)",
                          hovermode="x unified", paper_bgcolor='rgba(0,0,0,0)', 
                          plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig, use_container_width=True)
    
    with col_right:
        # ROOT CAUSE PIE WITH TOOLTIPS
        st.subheader("Loss Attribution")
        labels = ['Competitors', 'Pricing', 'Marketing', 'Product Fit']
        values = [40, 35, 15, 10]
        
        # Tooltips per section
        custom_data = [
            "Competitor 'X' launched 20% discount in March",
            "Average deal size dropped below industry baseline",
            "Ad-spend ROI decreased by 22% on Google Ads",
            "3 key features requested are currently in 'Backlog'"
        ]
        
        fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, 
                                         customdata=custom_data,
                                         hovertemplate="<b>%{label}</b><br>Impact: %{value}%<br>Note: %{customdata}<extra></extra>")])
        
        fig_pie.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', 
                              font_color="white", margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_pie, use_container_width=True)

with tab2:
    st.subheader("Predictive Recovery (Ghost-Line Comparison)")
    
    # SIMULATION LOGIC
    # Base recovery + price impact + marketing impact
    rec_multiplier = 1 + (mkt_boost/100 * 0.4) + (abs(price_adj)/100 * 0.3)
    simulated_rev = df["Revenue"] * rec_multiplier
    
    fig_sim = go.Figure()
    
    # The "Ghost Line" (Original Trend)
    fig_sim.add_trace(go.Scatter(x=df["Month"], y=df["Revenue"], name="Current (Do Nothing)", 
                                 line=dict(color='rgba(255,255,255,0.3)', dash='dot')))
    
    # The "Active Line" (Simulation)
    fig_sim.add_trace(go.Scatter(x=df["Month"], y=simulated_rev, name="Projected Recovery", 
                                 line=dict(color='#10b981', width=5),
                                 fill='tonexty', fillcolor='rgba(16, 185, 129, 0.1)'))
    
    fig_sim.update_layout(title="What-If Analysis: Strategy ROI", paper_bgcolor='rgba(0,0,0,0)', 
                          plot_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig_sim, use_container_width=True)
    
    st.success(f"Estimated Revenue Gap Closed: **${(simulated_rev.iloc[-1] - df['Revenue'].iloc[-1]):,.2f}**")

# --- ACTION PLAN ---
st.divider()
st.subheader("📋 AI-Generated Action Plan")
with st.expander("✅ Multi-step roadmap for Q3 Recovery", expanded=True):
    st.write("Based on the **Lead Decay** and **Competitor Pressure** detected:")
    st.markdown("""
    - 🚩 **CRITICAL:** Leads are dropping faster than Revenue. Launch a 'Re-engagement' email campaign by Friday.
    - 💡 **PRICING:** Your simulation shows a 5% price drop recovers 12% of lost volume. 
    - 🎯 **AD SPEND:** Increase LinkedIn ad spend targeting 'Churned' profiles.
    """)
