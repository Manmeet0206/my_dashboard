import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Sales Decline Tracker", layout="wide")

st.title("📉 Sales Decline Tracker Dashboard")

# Upload file
file = st.file_uploader("Upload your CSV file", type=["csv"])

if file:
    df = pd.read_csv(file)

    st.subheader("📊 Data Preview")
    st.dataframe(df.head())

    # Convert date
    df['Date'] = pd.to_datetime(df['Date'])

    # Sidebar filters
    st.sidebar.header("Filters")
    region = st.sidebar.multiselect("Select Region", df['Region'].unique())
    product = st.sidebar.multiselect("Select Product", df['Product'].unique())

    if region:
        df = df[df['Region'].isin(region)]
    if product:
        df = df[df['Product'].isin(product)]

    # KPI
    total_sales = df['Sales'].sum()
    avg_sales = df['Sales'].mean()

    # Decline %
    df_sorted = df.sort_values('Date')
    first = df_sorted['Sales'].iloc[0]
    last = df_sorted['Sales'].iloc[-1]
    decline_pct = ((first - last) / first) * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"{total_sales:,.0f}")
    col2.metric("Average Sales", f"{avg_sales:,.2f}")
    col3.metric("Decline %", f"{decline_pct:.2f}%")

    # Trend line
    st.subheader("📈 Sales Trend")
    fig, ax = plt.subplots()
    df.groupby('Date')['Sales'].sum().plot(ax=ax)
    st.pyplot(fig)

    # Monthly comparison
    st.subheader("📅 Monthly Comparison")
    df['Month'] = df['Date'].dt.to_period('M')
    monthly = df.groupby('Month')['Sales'].sum()

    fig2, ax2 = plt.subplots()
    monthly.plot(kind='bar', ax=ax2)
    st.pyplot(fig2)

    # Decline detection
    st.subheader("⚠️ Decline Detection")
    df['Change'] = df['Sales'].pct_change()
    decline_days = df[df['Change'] < 0]

    st.write(f"Days with decline: {len(decline_days)}")
    st.dataframe(decline_days[['Date', 'Sales', 'Change']])

    # Heatmap
    st.subheader("🔥 Correlation Heatmap")
    fig3, ax3 = plt.subplots()
    sns.heatmap(df.corr(numeric_only=True), annot=True, ax=ax3)
    st.pyplot(fig3)

else:
    st.info("Upload a CSV file to start")
