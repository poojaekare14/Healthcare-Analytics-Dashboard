import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ======================
# LOAD DATA (FIXED)
# ======================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "datasets", "healthcare_dataset.csv")
url="https://raw.githubusercontent.com/poojaekare14/Healthcare-Analytics-Dashboard/refs/heads/main/healthcare_dataset.csv"
df = pd.read_csv(url)

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(
    page_title="Healthcare Analytics Dashboard",
    page_icon="🏥",
    layout="wide"
)

# ======================
# STYLE
# ======================
st.markdown("""
<style>
.main {
    background-color: #F4F6F9;
}
.block-container {
    padding-top: 2rem;
}
h1, h2, h3 {
    color: #1f4e79;
}
</style>
""", unsafe_allow_html=True)

# ======================
# TITLE
# ======================
st.title("🏥 Healthcare Analytics Dashboard")
st.markdown("📊 Comprehensive Hospital Data Analysis & Insights")

st.divider()

# ======================
# KPI SECTION
# ======================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Patients", len(df))
col2.metric("Average Age", round(df["Age"].mean(), 1))
col3.metric("Average Billing", f"${round(df['Billing Amount'].mean(), 2)}")
col4.metric("Hospitals", df["Hospital"].nunique())

st.divider()

# ======================
# AGE DISTRIBUTION
# ======================
st.subheader("👥 Patient Age Distribution")

fig1 = px.histogram(
    df,
    x="Age",
    nbins=30,
    title="Age Distribution of Patients"
)
fig1.update_layout(bargap=0.1)
st.plotly_chart(fig1, use_container_width=True)

# ======================
# GENDER DISTRIBUTION
# ======================
st.subheader("⚧ Gender Distribution")

gender_count = df["Gender"].value_counts().reset_index()
gender_count.columns = ["Gender", "Count"]

fig2 = px.pie(
    gender_count,
    names="Gender",
    values="Count",
    title="Patient Gender Ratio"
)
st.plotly_chart(fig2, use_container_width=True)

# ======================
# MEDICAL CONDITIONS
# ======================
st.subheader("🩺 Medical Conditions Overview")

condition_counts = df["Medical Condition"].value_counts().reset_index()
condition_counts.columns = ["Condition", "Count"]

fig3 = px.bar(
    condition_counts,
    x="Condition",
    y="Count",
    color="Count",
    title="Most Common Medical Conditions"
)
fig3.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig3, use_container_width=True)

# ======================
# BILLING ANALYSIS
# ======================
st.subheader("💰 Billing Analysis")

col1, col2 = st.columns(2)

with col1:
    fig4 = px.histogram(
        df,
        x="Billing Amount",
        nbins=40,
        title="Billing Amount Distribution"
    )
    fig4.update_layout(bargap=0.1)
    st.plotly_chart(fig4, use_container_width=True)

with col2:
    avg_bill = df.groupby("Medical Condition")["Billing Amount"].mean().reset_index()

    fig5 = px.bar(
        avg_bill,
        x="Medical Condition",
        y="Billing Amount",
        color="Billing Amount",
        title="Average Billing per Condition"
    )
    fig5.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig5, use_container_width=True)

# ======================
# KEY INSIGHTS
# ======================
st.subheader("📌 Key Insights")

most_expensive_condition = df.groupby("Medical Condition")["Billing Amount"].mean().idxmax()
highest_avg_bill = df["Billing Amount"].mean()

st.success(f"🔴 Highest Cost Condition: {most_expensive_condition}")
st.info(f"💰 Overall Average Billing: ${round(highest_avg_bill, 2)}")

# ======================
# RECOMMENDATIONS
# ======================
st.subheader("📊 Recommendations for Healthcare Management")

st.markdown("""
### 🏥 Hospital Strategy Recommendations:

- 🔹 **Focus on High-Cost Diseases**
- 🔹 **Preventive Healthcare Programs**
- 🔹 **Age-Based Healthcare Planning**
- 🔹 **Billing Optimization**
- 🔹 **Resource Allocation**
- 🔹 **Health Awareness Campaigns**
""")

st.divider()

# ======================
# FOOTER
# ======================
st.caption("🏥 Healthcare Analytics Dashboard | Built with Streamlit + Plotly")