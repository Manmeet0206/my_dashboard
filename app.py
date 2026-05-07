import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="Sales Recovery Pro", layout="wide")

# --- ULTRA-MODERN CSS INJECTION ---
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background: linear-gradient(160deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.8);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Card-style containers */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }
    
    /* Customizing Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: linear-gradient(90deg, #3b82f6, #2563eb);
        color: white;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        color: white;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA GENERATION ---
@st.cache_data
def get_data():
    return pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Revenue": [12500, 11800, 10200, 9100, 8400, 7200],
        "Leads": [450, 420, 380, 310, 290, 240],
        "Churn": [2.1, 2.4, 3.1, 4.2, 5.8, 7.2]
    })

df = get_data()

# --- SIDEBAR ---
with st.sidebar:
    st.title("🚀 Simulation")
    st.file_uploader("Upload Sales Data")
    st.divider()
    price_adj = st.slider("Price Adjustment (%)", -20, 20, -5)
    mkt_boost = st.slider("Marketing Boost (%)", 0, 100, 25)
    st.button("Run Full Diagnostic")

# --- TOP METRICS ---
st.title("📉 Sales Decline Diagnostic")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Overall Decline", "-26.11%", "-4.2%")
c2.metric("Market Share Loss", "-11.5%", "Critical", delta_color="inverse")
c3.metric("Churn Rate", "7.26%", "+1.2%", delta_color="inverse")
c4.metric("Confidence Level", "99%", "High")

st.write("---")

# --- MAIN CONTENT ---
tab1, tab2 = st.tabs(["📊 Diagnostic View", "🧪 Strategy Simulator"])

with tab1:
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        # Styled Area Chart
        fig = px.area(df, x="Month", y="Revenue", title="Revenue vs. Lead Decay")
        fig.update_traces(line_color='#3b82f6', fillcolor='rgba(59, 130, 246, 0.2)')
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font_color="#f8fafc", margin=dict(l=0, r=0, t=40, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col_right:
        # Donut Chart for Loss Attribution
        labels = ['Competitors', 'Pricing', 'Marketing', 'Product Fit']
        values = [40, 35, 15, 10]
        fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6)])
        fig_pie.update_layout(
            showlegend=False, paper_bgcolor='rgba(0,0,0,0)',
            font_color="#f8fafc", margin=dict(l=0, r=0, t=30, b=0),
            annotations=[dict(text='Loss Origin', x=0.5, y=0.5, font_size=14, showarrow=False)]
        )
        st.plotly_chart(fig_pie, use_container_width=True)

with tab2:
    st.subheader("Predictive Recovery Curve")
    # Simulation Logic
    recovery_multiplier = 1 + (mkt_boost / 200) + (abs(price_adj) / 100)
    simulated_rev = df["Revenue"] * recovery_multiplier
    
    fig_sim = go.Figure()
    fig_sim.add_trace(go.Scatter(x=df["Month"], y=df["Revenue"], name="Current Trend", line=dict(dash='dash')))
    fig_sim.add_trace(go.Scatter(x=df["Month"], y=simulated_rev, name="Projected Recovery", line=dict(width=4, color='#10b981')))
    fig_sim.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig_sim, use_container_width=True)

# --- ACTION PLAN SECTION ---
st.write("---")
st.subheader("📋 AI-Generated Action Plan")
with st.expander("✅ Multi-step roadmap for Q3 Recovery", expanded=True):
    st.markdown("""
    1. **Immediate:** Price match competitor 'Tier A' offerings (Est. +4% Retention).
    2. **Short-term:** Reallocate $10k from Print to Social Retargeting.
    3. **Operational:** Implement automated churn alerts for high-value accounts.
    """)
