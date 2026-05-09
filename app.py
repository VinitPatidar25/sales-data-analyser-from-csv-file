import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from db import load_data_from_db
from ml_model import train_forecast
from insights import generate_insights

st.set_page_config(layout="wide")

st.title(" Intelligent Sales Analytics Platform")

# ----------- SIDEBAR -----------
st.sidebar.title("Data Source")

data_option = st.sidebar.radio(
    "Select Data Source",
    ["Upload CSV", "Upload Database"]
)

# ----------- LOAD DATA -----------

df = None

if data_option == "Upload CSV":
    file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
    if file:
        df = pd.read_csv(file)

elif data_option == "Upload Database":
    df = load_data_from_db()

# ----------- PROCESS -----------

if df is not None:

    df["Order_Date"] = pd.to_datetime(df["Order_Date"])

    # ----------- FILTERS -----------
    st.sidebar.header("Filters")

    region = st.sidebar.multiselect(
        "Region", df["Region"].unique(), df["Region"].unique()
    )

    df = df[df["Region"].isin(region)]

    # ----------- KPIs -----------
    st.subheader(" Key Metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Sales", int(df["Total_Sales"].sum()))
    col2.metric("Avg Sales", int(df["Total_Sales"].mean()))
    col3.metric("Orders", len(df))

    # ----------- LAYOUT -----------
    colA, colB = st.columns(2)

    # ----------- CHART -----------
    with colA:
        st.subheader("Sales Trend")

        trend = df.groupby("Order_Date")["Total_Sales"].sum()

        fig, ax = plt.subplots()
        ax.plot(trend.index, trend.values)

        st.pyplot(fig)

    # ----------- PRODUCT CHART -----------
    with colB:
        st.subheader("Top Products")

        prod = df.groupby("Product")["Total_Sales"].sum().sort_values()

        fig, ax = plt.subplots()
        prod.plot(kind="barh", ax=ax)

        st.pyplot(fig)

    # ----------- ML FORECAST -----------
    st.subheader("Forecast (Next 7 Days)")

    preds = train_forecast(trend.reset_index())

    st.line_chart(preds)

    # ----------- AI INSIGHTS -----------
    st.subheader(" AI Insights")

    insights = generate_insights(df)

    for i in insights:
        st.write("✔", i)

else:
    st.info("Upload data or connect to database")