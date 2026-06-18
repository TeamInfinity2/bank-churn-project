import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# -----------------------
# Page Config
# -----------------------
st.set_page_config(
    page_title="Bank Customer Churn Dashboard",
    page_icon="🏦",
    layout="wide"
)

# -----------------------
# Load Dataset (FIXED PATH)
# -----------------------
@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "BankChurners.csv")
    df = pd.read_csv(file_path)

    df["Churn"] = df["Attrition_Flag"].map({
        "Existing Customer": 0,
        "Attrited Customer": 1
    })

    return df

df = load_data()

# -----------------------
# Title
# -----------------------
st.title("🏦 Bank Customer Churn Analytics Dashboard")
st.markdown("### Business Intelligence | Customer Retention | Analytics")
st.divider()

# -----------------------
# Sidebar Filters
# -----------------------
st.sidebar.header("🔎 Filters")

gender = st.sidebar.multiselect("Gender", df["Gender"].unique(), df["Gender"].unique())
income = st.sidebar.multiselect("Income Category", df["Income_Category"].unique(), df["Income_Category"].unique())
card = st.sidebar.multiselect("Card Category", df["Card_Category"].unique(), df["Card_Category"].unique())

filtered_df = df[
    (df["Gender"].isin(gender)) &
    (df["Income_Category"].isin(income)) &
    (df["Card_Category"].isin(card))
]

# -----------------------
# KPI Metrics
# -----------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 Customers", len(filtered_df))
col2.metric("📉 Churn Rate", f"{filtered_df['Churn'].mean()*100:.2f}%")
col3.metric("🎂 Avg Age", f"{filtered_df['Customer_Age'].mean():.1f}")
col4.metric("💳 Avg Credit", f"${filtered_df['Credit_Limit'].mean():,.0f}")

st.divider()

# -----------------------
# Charts Row 1
# -----------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Churn Distribution")
    fig, ax = plt.subplots()
    sns.countplot(x="Attrition_Flag", data=filtered_df, ax=ax)
    plt.xticks(rotation=10)
    st.pyplot(fig)

with col2:
    st.subheader("👨 Gender vs Churn")
    fig, ax = plt.subplots()
    sns.barplot(x="Gender", y="Churn", data=filtered_df, ax=ax)
    st.pyplot(fig)

st.divider()

# -----------------------
# Charts Row 2
# -----------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎂 Age Distribution")
    fig, ax = plt.subplots()
    sns.histplot(filtered_df["Customer_Age"], bins=20, kde=True, ax=ax)
    st.pyplot(fig)

with col2:
    st.subheader("💳 Credit Limit Distribution")
    fig, ax = plt.subplots()
    sns.histplot(filtered_df["Credit_Limit"], bins=20, kde=True, ax=ax)
    st.pyplot(fig)

st.divider()

# -----------------------
# Heatmap
# -----------------------
st.subheader("🔥 Correlation Heatmap")

numeric_df = filtered_df.select_dtypes(include=["int64", "float64"])

fig, ax = plt.subplots(figsize=(10,5))
sns.heatmap(numeric_df.corr(), cmap="coolwarm", ax=ax)

st.pyplot(fig)

st.divider()

# -----------------------
# Data Preview
# -----------------------
st.subheader("📋 Data Table")
st.dataframe(filtered_df)

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Data",
    csv,
    "filtered_data.csv",
    "text/csv"
)
