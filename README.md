# HR Employee Attrition Analytics

An end-to-end data analytics project that pipelines raw HR data through cleaning, a live cloud database, SQL analysis, and a machine learning model — all deployed as an interactive web app.

**Live App:** https://hr-attrition-analytics-qz2sjldqycpy3viu7p29kf.streamlit.app/

## Overview

This project analyzes employee attrition patterns using the IBM HR Analytics Employee Attrition dataset (1,470 employees) and builds a predictive model to flag employees at risk of leaving. The final product is a two-page Streamlit dashboard: one page for exploratory analytics, and one for live, individual attrition-risk scoring.

## Tech Stack

- **Python** (Pandas) — data cleaning and feature engineering
- **PostgreSQL** (hosted on Supabase) — cloud data warehouse
- **SQL** — attrition analysis queries (department, tenure, overtime, cost-of-attrition)
- **Scikit-learn** — logistic regression risk model
- **Streamlit** — interactive web app, deployed on Streamlit Community Cloud
- **Plotly** — dashboard visualizations

## Pipeline

1. **ETL**: Raw CSV cleaned in Python — dropped constant columns, engineered readable labels for ordinal fields, created age/tenure buckets and a binary attrition flag.
2. **Storage**: Cleaned dataset loaded into a PostgreSQL database on Supabase.
3. **Analysis**: SQL queries computed attrition rate by department, tenure group, overtime status, and job role.
4. **Modeling**: A logistic regression model (scaled features, balanced class weights to handle the 84/16 class imbalance) predicts attrition risk per employee.
5. **App**: A Streamlit app connects live to the database for the dashboard and loads the saved model for real-time predictions.

## Key Findings

- **Overall attrition rate: 16.1%** (237 of 1,470 employees)
- **Sales has the highest attrition** (20.6%), followed by HR (19.1%); R&D is lowest (13.8%)
- **The first 2 years are the highest-risk period**: 29.8% attrition vs. single digits/low teens after 6+ years
- **OverTime is the strongest driver**: employees working overtime leave at ~3x the rate of those who don't (30.5% vs. 10.4%)
- **Cost varies sharply by role**: Managers and Research Directors who leave cost far more per head than Lab Technicians or Sales Representatives, despite lower headcount loss

## Model Performance

- **ROC-AUC: 0.81**
- **Recall (attrition class): 77%** — correctly identifies most employees who are likely to leave, prioritizing catching at-risk employees over minimizing false alarms (appropriate for an HR early-warning use case)

## App Features

- **Dashboard**: KPI summary + four interactive charts (department, tenure, overtime, job role)
- **Risk Predictor**: Select any employee to see their live predicted attrition risk (%) with a color-coded risk level

## Running Locally

```bash
git clone https://github.com/KTSneha/hr-attrition-analytics.git
cd hr-attrition-analytics
pip install -r requirements.txt
```

Create a `.env` file in the project root:
```
DATABASE_URL=your_postgresql_connection_string
```

Then run:
```bash
streamlit run app.py
```

## Dataset

[IBM HR Analytics Employee Attrition & Performance](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset) (Kaggle)
