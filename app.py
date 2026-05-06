import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sales Decline Tracker", layout="wide")

st.title("📉 Sales Decline Tracker PRO")

file = st.file_uploader("Upload CSV", type=["csv"])

if file:
    df = pd.read_csv(file)
    df['Date'] = pd.to_datetime(df['Date'])

    # Sidebar filters
    st.sidebar.header("Filters")

    date_range = st.sidebar.date_input("Select Date Range", [df['Date'].min(), df['Date'].max()])
    region = st.sidebar.multiselect("Region", df['Region'].unique())
    product = st.sidebar.multiselect("Product", df['Product'].unique())

    # Apply filters
    if len(date_range) == 2:
        df = df[(df['Date'] >= pd.to_datetime(date_range[0])) & (df['Date'] <= pd.to_datetime(date_range[1]))]

    if region:
        df = df[df['Region'].isin(region)]

    if product:
        df = df[df['Product'].isin(product)]

    # KPIs
    total_sales = df['Sales'].sum()
    avg_sales = df['Sales'].mean()

    df_sorted = df.sort_values('Date')
    first = df_sorted['Sales'].iloc[0]
    last = df_sorted['Sales'].iloc[-1]
    decline = ((first - last) / first) * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"{total_sales:,.0f}")
    col2.metric("Average Sales", f"{avg_sales:,.2f}")
    col3.metric("Decline %", f"{decline:.2f}%")

    # Trend chart (interactive)
    st.subheader("📈 Sales Trend")
    trend = df.groupby('Date')['Sales'].sum().reset_index()
    fig = px.line(trend, x='Date', y='Sales')
    st.plotly_chart(fig, use_container_width=True)

    # Monthly chart
    st.subheader("📅 Monthly Performance")
    df['Month'] = df['Date'].dt.to_period('M').astype(str)
    monthly = df.groupby('Month')['Sales'].sum().reset_index()
    fig2 = px.bar(monthly, x='Month', y='Sales')
    st.plotly_chart(fig2, use_container_width=True)

    # Top & low products
    st.subheader("🏆 Product Performance")
    prod = df.groupby('Product')['Sales'].sum().reset_index()
    top = prod.sort_values('Sales', ascending=False).head(5)
    low = prod.sort_values('Sales').head(5)

    col4, col5 = st.columns(2)
    col4.write("Top Products")
    col4.dataframe(top)

    col5.write("Low Performing Products")
    col5.dataframe(low)

    # Decline alerts
    st.subheader("⚠️ Decline Alerts")
    df['Change'] = df['Sales'].pct_change()
    decline_days = df[df['Change'] < 0]

    st.write(f"Decline instances: {len(decline_days)}")
    st.dataframe(decline_days[['Date', 'Sales', 'Change']])

    # Smart insight
    st.subheader("🧠 Smart Insights")

    if decline > 0:
        st.warning("Sales are declining overall. Focus on low performing products.")
    else:
        st.success("Sales trend is stable or improving.")

    # Download button
    st.subheader("📥 Download Filtered Data")
    st.download_button("Download CSV", df.to_csv(index=False), file_name="filtered_data.csv")

else:
    st.info("Upload CSV to begin")
