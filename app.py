import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import os
import joblib
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')

st.set_page_config(page_title="HR Attrition Analytics", layout="wide")

@st.cache_resource
def get_engine():
    return create_engine(db_url)

@st.cache_resource
def load_model_artifacts():
    model = joblib.load('models/attrition_model.pkl')
    scaler = joblib.load('models/scaler.pkl')
    label_encoders = joblib.load('models/label_encoders.pkl')
    feature_columns = joblib.load('models/feature_columns.pkl')
    return model, scaler, label_encoders, feature_columns

engine = get_engine()
model, scaler, label_encoders, feature_columns = load_model_artifacts()

st.title("HR Employee Attrition Analytics")

tab1, tab2 = st.tabs(["📊 Dashboard", "🔮 Risk Predictor"])

# ---------------- TAB 1: DASHBOARD ----------------
with tab1:
    kpi_query = '''
    SELECT 
        COUNT(*) AS total_employees,
        SUM(CASE WHEN "Attrition" = 'Yes' THEN 1 ELSE 0 END) AS attrition_count,
        ROUND(100.0 * SUM(CASE WHEN "Attrition" = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate_pct
    FROM employees;
    '''
    kpis = pd.read_sql(kpi_query, engine).iloc[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Employees", int(kpis['total_employees']))
    col2.metric("Employees Left", int(kpis['attrition_count']))
    col3.metric("Attrition Rate", f"{kpis['attrition_rate_pct']}%")

    st.markdown("---")

    col1, col2 = st.columns(2)

    dept_query = '''
    SELECT "Department", COUNT(*) AS total,
        ROUND(100.0 * SUM(CASE WHEN "Attrition" = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate_pct
    FROM employees GROUP BY "Department" ORDER BY attrition_rate_pct DESC;
    '''
    dept_df = pd.read_sql(dept_query, engine)
    fig1 = px.bar(dept_df, x="Department", y="attrition_rate_pct",
                  title="Attrition Rate by Department", text="attrition_rate_pct")
    col1.plotly_chart(fig1, use_container_width=True)

    tenure_query = '''
    SELECT "TenureGroup",
        ROUND(100.0 * SUM(CASE WHEN "Attrition" = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate_pct
    FROM employees GROUP BY "TenureGroup" ORDER BY "TenureGroup";
    '''
    tenure_df = pd.read_sql(tenure_query, engine)
    fig2 = px.bar(tenure_df, x="TenureGroup", y="attrition_rate_pct",
                  title="Attrition Rate by Tenure", text="attrition_rate_pct")
    col2.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    ot_query = '''
    SELECT "OverTime",
        ROUND(100.0 * SUM(CASE WHEN "Attrition" = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate_pct
    FROM employees GROUP BY "OverTime";
    '''
    ot_df = pd.read_sql(ot_query, engine)
    fig3 = px.bar(ot_df, x="OverTime", y="attrition_rate_pct",
                  title="Attrition Rate: OverTime vs No OverTime", text="attrition_rate_pct")
    col3.plotly_chart(fig3, use_container_width=True)

    role_query = '''
    SELECT "JobRole", COUNT(*) AS attritions, ROUND(AVG("MonthlyIncome"), 0) AS avg_monthly_income
    FROM employees WHERE "Attrition" = 'Yes' GROUP BY "JobRole" ORDER BY attritions DESC;
    '''
    role_df = pd.read_sql(role_query, engine)
    fig4 = px.bar(role_df, x="JobRole", y="attritions",
                  title="Attrition Count by Job Role", text="attritions")
    fig4.update_layout(xaxis_tickangle=-45)
    col4.plotly_chart(fig4, use_container_width=True)

# ---------------- TAB 2: RISK PREDICTOR ----------------
with tab2:
    st.subheader("Predict Attrition Risk for an Employee")

    employees_df = pd.read_sql('SELECT * FROM employees ORDER BY "EmployeeNumber"', engine)

    emp_ids = employees_df['EmployeeNumber'].tolist()
    selected_id = st.selectbox("Select Employee Number", emp_ids)

    emp_row = employees_df[employees_df['EmployeeNumber'] == selected_id].iloc[0]

    st.write("**Employee snapshot:**")
    snap_cols = st.columns(4)
    snap_cols[0].write(f"Department: {emp_row['Department']}")
    snap_cols[1].write(f"Job Role: {emp_row['JobRole']}")
    snap_cols[2].write(f"Years at Company: {emp_row['YearsAtCompany']}")
    snap_cols[3].write(f"OverTime: {emp_row['OverTime']}")

    if st.button("Predict Risk"):
        # Build feature row matching training columns
        drop_cols = ['Attrition', 'AttritionFlag', 'EmployeeNumber', 'EducationLabel',
                     'EnvironmentSatisfactionLabel', 'JobInvolvementLabel', 'JobSatisfactionLabel',
                     'RelationshipSatisfactionLabel', 'WorkLifeBalanceLabel', 'PerformanceRatingLabel',
                     'AgeGroup', 'TenureGroup']
        emp_features = emp_row.drop(labels=[c for c in drop_cols if c in emp_row.index])
        emp_features = emp_features[feature_columns]

        emp_features = emp_features.copy()
        for col, le in label_encoders.items():
            if col in emp_features.index:
                emp_features[col] = le.transform([emp_features[col]])[0]

        X_input = emp_features.values.reshape(1, -1)
        X_scaled = scaler.transform(X_input)

        risk_proba = model.predict_proba(X_scaled)[0][1]
        risk_pct = round(risk_proba * 100, 1)

        st.metric("Attrition Risk", f"{risk_pct}%")

        if risk_pct >= 50:
            st.error("⚠️ High risk — recommend HR follow-up")
        elif risk_pct >= 25:
            st.warning("🟡 Moderate risk — monitor")
        else:
            st.success("🟢 Low risk")