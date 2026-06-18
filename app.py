import streamlit as st
import matplotlib.pyplot as plt

# -----------------------
# Page Configuration
# -----------------------
st.set_page_config(
    page_title="Bank Customer Churn Dashboard",
    page_icon="🏦",
    layout="wide"
)

# -----------------------
# Load Dataset
# -----------------------
@st.cache_data
def load_data():
    df = pd.read_csv("BankChurners.csv")

    df["Churn"] = df["Attrition_Flag"].map({
        "Existing Customer":0,
        "Attrited Customer":1
    })

    return df

df = load_data()

# -----------------------
# Dashboard Title
# -----------------------

st.title("🏦 Bank Customer Churn Analytics Dashboard")

st.markdown("### Business Intelligence | Customer Retention | Data Analytics")

st.divider()

# -----------------------
# Sidebar Filters
# -----------------------

st.sidebar.header("🔎 Filter Customers")

gender = st.sidebar.multiselect(
    "Gender",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

income = st.sidebar.multiselect(
    "Income Category",
    options=df["Income_Category"].unique(),
    default=df["Income_Category"].unique()
)

card = st.sidebar.multiselect(
    "Card Category",
    options=df["Card_Category"].unique(),
    default=df["Card_Category"].unique()
)

filtered_df = df[
    (df["Gender"].isin(gender)) &
    (df["Income_Category"].isin(income)) &
    (df["Card_Category"].isin(card))
]


# -----------------------
# KPI Cards
# -----------------------

total_customers = len(filtered_df)
churn_rate = filtered_df["Churn"].mean() * 100
avg_age = filtered_df["Customer_Age"].mean()
avg_credit = filtered_df["Credit_Limit"].mean()
total_transactions = filtered_df["Total_Trans_Amt"].sum()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("👥 Customers", f"{total_customers:,}")

col2.metric("📉 Churn Rate", f"{churn_rate:.2f}%")

col3.metric("🎂 Avg Age", f"{avg_age:.1f}")

col4.metric("💳 Avg Credit", f"${avg_credit:,.0f}")

col5.metric("💰 Transactions", f"${total_transactions:,.0f}")

st.divider()


# -----------------------
# Row 2 Charts
# -----------------------

col3, col4 = st.columns(2)

with col3:

    st.subheader("💰 Income Category vs Churn")

    fig, ax = plt.subplots(figsize=(7,4))

    sns.barplot(
        x="Income_Category",
        y="Churn",
        data=filtered_df,
        palette="viridis",
        ax=ax
    )

    plt.xticks(rotation=45)

    st.pyplot(fig)


with col4:

    st.subheader("💳 Card Category vs Churn")

    fig, ax = plt.subplots(figsize=(6,4))

    sns.barplot(
        x="Card_Category",
        y="Churn",
        data=filtered_df,
        palette="rocket",
        ax=ax
    )

    st.pyplot(fig)

st.divider()

# -----------------------
# Row 3 Charts
# -----------------------

col5, col6 = st.columns(2)

with col5:
    st.subheader("🎂 Customer Age Distribution")

    fig, ax = plt.subplots(figsize=(6,4))
    sns.histplot(filtered_df["Customer_Age"], bins=20, kde=True, ax=ax)

    st.pyplot(fig)

with col6:
    st.subheader("💳 Credit Limit Distribution")

    fig, ax = plt.subplots(figsize=(6,4))
    sns.histplot(filtered_df["Credit_Limit"], bins=20, kde=True, ax=ax)

    st.pyplot(fig)

st.divider()

# -----------------------
# Correlation Heatmap
# -----------------------

st.subheader("🔥 Correlation Heatmap")

numeric_df = filtered_df.select_dtypes(include=["int64", "float64"])

fig, ax = plt.subplots(figsize=(12,7))

sns.heatmap(
    numeric_df.corr(),
    cmap="coolwarm",
    annot=False,
    ax=ax
)

st.pyplot(fig)

st.divider()


# -----------------------
# Dataset Preview
# -----------------------

st.subheader("📋 Filtered Customer Data")

st.dataframe(filtered_df)

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="Filtered_Bank_Customers.csv",
    mime="text/csv"
)

