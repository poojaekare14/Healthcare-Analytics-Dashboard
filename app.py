import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Healthcare Intelligence Dashboard", page_icon="🏥", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv(r"datasets\healthcare_dataset.csv")
    
    df = df.drop_duplicates()

    bins = [0,18,35,50,65,100]
    labels = ["Child","Young Adult","Adult","Middle Age","Senior"]
    df["Age Group"] = pd.cut(df["Age"], bins=bins, labels=labels, include_lowest=True)
    return df

df = load_data()

st.markdown("""
<style>

/* Main Background */
.stApp{
background: linear-gradient(
-45deg,
#000000,
#0f172a,
#111827,
#1e293b
);
background-size: 400% 400%;
animation: gradient 15s ease infinite;
color: white !important;
}

@keyframes gradient{
0% {background-position:0% 50%;}
50% {background-position:100% 50%;}
100% {background-position:0% 50%;}
}

/* All Text */
h1,h2,h3,h4,h5,h6,p,label,span{
color:white !important;
}

/* Metric Cards */
div[data-testid="metric-container"]{
background: rgba(255,255,255,0.08);
backdrop-filter: blur(10px);
border-radius: 15px;
padding: 15px;
border: 1px solid rgba(255,255,255,0.15);
box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

/* Metric Values */
div[data-testid="metric-container"] label{
color:white !important;
}

div[data-testid="metric-container"] div{
color:white !important;
}

/* Sidebar */
section[data-testid="stSidebar"]{
background-color:#0f172a;
}

/* Tabs */
button[data-baseweb="tab"]{
color:white !important;
font-weight:bold;
}

/* Tables */
[data-testid="stDataFrame"]{
background-color:white;
border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

st.title("🏥 Healthcare Intelligence Dashboard")
st.caption("Patient Analytics • Disease Intelligence • Financial Insights")

st.sidebar.header("Filters")

gender = st.sidebar.multiselect("Gender", df["Gender"].unique(), default=df["Gender"].unique())
condition = st.sidebar.multiselect("Medical Condition", df["Medical Condition"].unique(), default=df["Medical Condition"].unique())
insurance = st.sidebar.multiselect("Insurance Provider", df["Insurance Provider"].unique(), default=df["Insurance Provider"].unique())
admission = st.sidebar.multiselect("Admission Type", df["Admission Type"].unique(), default=df["Admission Type"].unique())

st.sidebar.markdown("---")
st.sidebar.subheader("📂 App Information")

with st.sidebar.expander("Dataset Information"):

    st.write(f"**Rows:** {df.shape[0]}")
    st.write(f"**Columns:** {df.shape[1]}")

    st.write("### Dataset Preview")
    st.dataframe(df.head())

    st.write("### Column Names")
    st.write(list(df.columns))

    st.write("### Missing Values")

    missing_df = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isnull().sum().values
    })

    st.dataframe(missing_df)

csv = df.to_csv(index=False).encode("utf-8")

st.sidebar.download_button(
    label="📥 Download Dataset",
    data=csv,
    file_name="healthcare_dataset.csv",
    mime="text/csv"
)

filtered_df = df[
(df["Gender"].isin(gender)) &
(df["Medical Condition"].isin(condition)) &
(df["Insurance Provider"].isin(insurance)) &
(df["Admission Type"].isin(admission))
]

c1,c2,c3,c4,c5,c6 = st.columns(6)
c1.metric("Patients", len(filtered_df))
c2.metric("Hospitals", filtered_df["Hospital"].nunique())
c3.metric("Doctors", filtered_df["Doctor"].nunique())
c4.metric("Avg Age", round(filtered_df["Age"].mean(),1))
c5.metric("Avg Billing", f"${filtered_df['Billing Amount'].mean():,.0f}")
c6.metric("Top Disease", filtered_df["Medical Condition"].mode()[0])

tabs = st.tabs([
    "App Information",
    "🏠 Overview",
    "👥 Demographics",
    "🩺 Medical Analysis",
    "🏥 Hospital Analysis",
    "💰 Financial Analysis",
    "📈 Advanced Analytics",
    "📋 Insights"
])

# =====================================================
# APP INFORMATION
# =====================================================

with tabs[0]:

    st.header("📊 Dataset Information")

    col1,col2,col3 = st.columns(3)

    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())

    st.markdown("---")

    st.subheader("Dataset Preview")
    st.dataframe(df.head(), width="stretch")

    st.subheader("Dataset Columns")
    st.write(list(df.columns))

    st.subheader("Missing Values")

    missing_df = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isnull().sum().values
    })

    st.dataframe(missing_df, width="stretch")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Dataset",
        csv,
        "healthcare_dataset.csv",
        "text/csv"
    )

    st.markdown("---")

    st.subheader("Gender Distribution")

    gender_df = filtered_df["Gender"].value_counts().reset_index()
    gender_df.columns = ["Gender","Count"]

    fig = px.pie(
        gender_df,
        names="Gender",
        values="Count",
        hole=0.5
    )

    st.plotly_chart(fig, width="stretch")

    st.info("""
    Observation:
    • Male and female patient counts are nearly balanced.
    • Healthcare services should be planned equally for both groups.
    """)

    st.subheader("Admission Type Distribution")

    admission_df = filtered_df["Admission Type"].value_counts().reset_index()
    admission_df.columns = ["Admission Type","Count"]

    fig = px.pie(
        admission_df,
        names="Admission Type",
        values="Count",
        hole=0.5
    )

    st.plotly_chart(fig, width="stretch")

    st.success("""
    Business Insight:
    • Emergency admissions require continuous hospital preparedness.
    • Resource allocation should prioritize emergency services.
    """)
    

with tabs[1]:
    a,b = st.columns(2)

    a.plotly_chart(
        px.histogram(filtered_df, x="Age", title="Age Distribution"),
        width="stretch"
    )

    b.plotly_chart(
        px.pie(filtered_df, names="Gender", hole=.5, title="Gender Distribution"),
        width="stretch"
    )

    st.markdown("### 📌 Observation")
    st.info("""
    • The patient population spans multiple age groups.  
    • Gender distribution is balanced.  
    • Adults and seniors dominate healthcare demand.
    """)

    st.markdown("### 💡 Business Insight")
    st.success("""
    • Build age-specific healthcare programs.  
    • Plan resources for senior care demand.  
    • Ensure gender-balanced service delivery.
    """)

with tabs[2]:
    age_df = filtered_df["Age Group"].value_counts().reset_index()
    age_df.columns = ["Age Group", "count"]
    st.plotly_chart(px.bar(age_df,x="Age Group",y="count",title="Age Group Distribution"),width="stretch")

    blood_df = filtered_df["Blood Type"].value_counts().reset_index()
    blood_df.columns = ["Blood Type", "count"]
    st.plotly_chart(px.bar(blood_df,x="Blood Type",y="count",title="Blood Type Distribution"),width="stretch")
    
    st.markdown("### 📌 Observation")
    st.info("""
    • Adult and senior citizens form the majority of the patient population.
    • Blood groups are fairly distributed across patients without major concentration in a single category.
    • The demographic profile indicates a growing need for chronic care and preventive services.
    """)
    st.markdown("### 💡 Business Insight")
    st.success("""
    • Hospitals should maintain adequate blood bank inventories across all major blood groups.
    • Preventive healthcare campaigns should target middle-aged and senior populations.
    • Demographic trends can help forecast future healthcare demand.
   """)

with tabs[3]:
    med = filtered_df["Medical Condition"].value_counts().reset_index()
    med.columns = ["Medical Condition", "count"]
    st.plotly_chart(px.bar(med,x="Medical Condition",y="count",title="Medical Condition Distribution"),width="stretch")

    st.subheader("Disease Distribution Across Gender")

    gender_disease = pd.crosstab(
        filtered_df["Medical Condition"],
        filtered_df["Gender"]
    )

    st.bar_chart(gender_disease)
    st.markdown("### 📌 Observation")
    st.info("""
    • Certain medical conditions occur more frequently than others.
    • Chronic illnesses contribute significantly to hospital admissions.
    • Disease prevalence highlights major healthcare challenges within the patient population.
    """)
    st.markdown("### 💡 Business Insight")
    st.success("""
    • Investment in chronic disease management programs can reduce long-term treatment costs.
    • Early diagnosis and preventive care initiatives can improve patient outcomes.
    • Healthcare organizations should prioritize resources for high-prevalence conditions.
    """)

with tabs[4]:
    hosp = filtered_df["Hospital"].value_counts().head(10).reset_index()
    st.plotly_chart(px.bar(hosp,x="count",y="Hospital",orientation="h",title="Top Hospitals"),width="stretch")
    
    st.subheader("Top Doctors")

    doc = (
        filtered_df["Doctor"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    doc.columns = ["Doctor","Count"]

    fig = px.bar(
        doc,
        x="Count",
        y="Doctor",
        orientation="h",
        title="Top Doctors by Patient Count"
    )

    st.plotly_chart(fig, width="stretch")
    st.markdown("### 📌 Observation")
    st.info("""
    • Patient load is concentrated in few hospitals.
    • Top doctors handle majority of patients.
    • Imbalance in hospital utilization exists.
    """)

    st.markdown("### 💡 Business Insight")
    st.success("""
    • Improve load balancing across hospitals.
    • Increase staff in high-demand hospitals.
    • Replicate best practices from top hospitals.
    """)

with tabs[5]:
    bill = filtered_df.groupby("Medical Condition")["Billing Amount"].mean().reset_index()
    st.plotly_chart(px.bar(bill,x="Medical Condition",y="Billing Amount",title="Average Billing by Disease"),width="stretch")
    
    st.subheader("Billing Amount Distribution")

    fig = px.histogram(
        filtered_df,
        x="Billing Amount",
        nbins=30,
        title="Billing Amount Distribution"
    )

    st.plotly_chart(fig, width="stretch")
    st.markdown("### 📌 Observation")
    st.info("""
    • Average billing amounts vary considerably across medical conditions.
    • Certain diseases require significantly higher treatment costs.
    • Healthcare expenditure is influenced by disease complexity and treatment requirements.
    """)
    st.markdown("### 💡 Business Insight")
    st.success("""
    • Cost optimization efforts should focus on high-expense medical conditions.
    • Financial forecasting can be improved using disease-specific billing trends.
    • Billing analysis helps hospitals identify areas for cost reduction and resource efficiency.
    """)

with tabs[6]:
    ins = filtered_df["Insurance Provider"].value_counts().reset_index()
    st.plotly_chart(px.bar(ins,x="Insurance Provider",y="count",title="Insurance Provider Distribution"),width="stretch")

    st.markdown("### 📌 Observation")
    st.info("""
    • A few insurance providers account for a large share of patient coverage.
    • Insurance participation is widespread among patients.
    • Coverage distribution highlights the importance of insurer partnerships.
    """)
    st.markdown("### 💡 Business Insight")
    st.success("""
    • Strengthening relationships with major insurance providers can improve claim processing efficiency.
    • Insurance trend analysis can support strategic partnership decisions.
    • Better insurance integration can enhance patient satisfaction and accessibility.
    """)

with tabs[7]:
    st.markdown("### 🔑 Key Findings")
    st.success("""
    • Adult and senior patients form the majority of the patient population.
    • Chronic medical conditions account for a significant portion of healthcare demand.
    • Healthcare costs vary substantially across diseases.
    • Patient admissions are concentrated among a subset of hospitals.
    • Insurance coverage is dominated by a few major providers.
    """)

    st.markdown("### 📋 Recommendations")
    st.info("""
    • Expand preventive healthcare initiatives.
    • Strengthen chronic disease management programs.
    • Optimize hospital resource allocation.
    • Improve insurance collaboration and claim efficiency.
    • Use financial analytics to control treatment costs and improve operational performance.
    """)