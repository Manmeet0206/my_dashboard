import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime
from scipy import stats
from sklearn.linear_model import LinearRegression
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

# ---------------- LOGIN SYSTEM ----------------
def login():
    st.title("🔐 AI Dashboard Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state["logged_in"] = True
        else:
            st.error("Invalid credentials")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()

# ---------------- DATA ----------------
@st.cache_data
def generate_data():
    dates = pd.date_range("2026-01-01", periods=120)
    trend = np.linspace(100, 130, 90).tolist() + np.linspace(130, 70, 30).tolist()
    noise = np.random.normal(0, 6, 120)
    sales = np.array(trend) + noise

    df = pd.DataFrame({"Date": dates, "Sales": sales})
    return df

df = generate_data()

# ---------------- ANOMALY ----------------
df["Z_score"] = np.abs(stats.zscore(df["Sales"]))
df["Anomaly"] = df["Z_score"] > 2

# ---------------- FORECAST ----------------
X = np.array(range(len(df))).reshape(-1, 1)
y = df["Sales"].values

model = LinearRegression()
model.fit(X, y)

future = model.predict(np.array(range(len(df), len(df)+30)).reshape(-1,1))
future_dates = pd.date_range(df["Date"].iloc[-1], periods=30)

# ---------------- PDF REPORT FUNCTION ----------------
def create_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("Sales Dashboard Report", styles['Title']))
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"Generated on: {datetime.now()}", styles['Normal']))
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"Total Sales Records: {len(df)}", styles['Normal']))
    content.append(Paragraph(f"Detected Anomalies: {df['Anomaly'].sum()}", styles['Normal']))
    content.append(Paragraph(f"Average Sales: {df['Sales'].mean():.2f}", styles['Normal']))

    doc.build(content)
    buffer.seek(0)
    return buffer

# ---------------- UI ----------------
st.title("📊 AI Sales Intelligence Dashboard")

col1, col2, col3 = st.columns(3)
col1.metric("Current Sales", f"{df['Sales'].iloc[-1]:.1f}")
col2.metric("Anomalies", int(df["Anomaly"].sum()))
col3.metric("Avg Sales", f"{df['Sales'].mean():.1f}")

st.divider()

# ---------------- CHART ----------------
fig = go.Figure()

fig.add_trace(go.Scatter(x=df["Date"], y=df["Sales"], name="Sales"))

fig.add_trace(go.Scatter(
    x=df[df["Anomaly"]]["Date"],
    y=df[df["Anomaly"]]["Sales"],
    mode="markers",
    name="Anomaly",
    marker=dict(color="red", size=8)
))

fig.add_trace(go.Scatter(
    x=future_dates,
    y=future,
    name="Forecast",
    line=dict(dash="dash", color="green")
))

st.plotly_chart(fig, use_container_width=True)

# ---------------- DOWNLOAD PDF ----------------
st.subheader("📄 Export Report")

pdf = create_pdf()

st.download_button(
    label="Download PDF Report",
    data=pdf,
    file_name="sales_report.pdf",
    mime="application/pdf"
)
