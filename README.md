<div align="center">

# 👥 HR Employee Attrition Analytics

### An end-to-end data analytics pipeline — from raw data to a live, ML-powered web app

[![Streamlit App](https://img.shields.io/badge/🚀_Live_App-Streamlit-FF4B4B?style=for-the-badge)](https://hr-attrition-analytics-qz2sjldqycpy3viu7p29kf.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://supabase.com)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML_Model-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)

**[🔗 View Live App](https://hr-attrition-analytics-qz2sjldqycpy3viu7p29kf.streamlit.app/)**

</div>

---

## 📌 Overview

This project analyzes employee attrition patterns using the **IBM HR Analytics Employee Attrition** dataset (1,470 employees) and builds a predictive model to flag employees at risk of leaving. The final product is a two-page Streamlit dashboard: one page for exploratory analytics, and one for **live, individual attrition-risk scoring**.

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python (Pandas, NumPy) |
| **Database** | PostgreSQL (hosted on Supabase) |
| **Analysis** | SQL |
| **Machine Learning** | Scikit-learn (Logistic Regression) |
| **Visualization** | Plotly |
| **Web App** | Streamlit (deployed on Streamlit Community Cloud) |

## 🔄 Pipeline

```
Raw CSV → Python ETL → PostgreSQL (Supabase) → SQL Analysis → ML Model → Streamlit App
```

1. **ETL** — Raw CSV cleaned in Python: dropped constant columns, engineered readable labels for ordinal fields, created age/tenure buckets and a binary attrition flag.
2. **Storage** — Cleaned dataset loaded into a PostgreSQL database on Supabase.
3. **Analysis** — SQL queries computed attrition rate by department, tenure group, overtime status, and job role.
4. **Modeling** — A logistic regression model (scaled features, balanced class weights) predicts attrition risk per employee.
5. **App** — A Streamlit app connects live to the database for the dashboard and loads the saved model for real-time predictions.

## 📊 Key Findings

| Insight | Finding |
|---|---|
| 📉 Overall attrition rate | **16.1%** (237 of 1,470 employees) |
| 🏢 Highest-risk department | **Sales** — 20.6% attrition |
| ⏳ Highest-risk tenure | **0–2 years** — 29.8% attrition |
| ⏰ Overtime impact | Employees working overtime leave at **~3x the rate** (30.5% vs. 10.4%) |
| 💰 Cost hotspot | Managers & Research Directors who leave cost far more per head than junior roles, despite lower headcount loss |

## 🎯 Model Performance

<div align="center">

| Metric | Score |
|---|---|
| **ROC-AUC** | 0.81 |
| **Recall (Attrition = Yes)** | 77% |

</div>

The model prioritizes **catching at-risk employees** (high recall) over minimizing false alarms — the right trade-off for an HR early-warning tool, where missing a likely departure is costlier than a false positive.

## ✨ App Features

- **📊 Dashboard** — KPI summary + four interactive charts (department, tenure, overtime, job role)
- **🔮 Risk Predictor** — Select any employee to see their live predicted attrition risk (%) with a color-coded risk level (🟢 Low / 🟡 Moderate / 🔴 High)

## 🚀 Running Locally

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

## 📁 Dataset

[IBM HR Analytics Employee Attrition & Performance](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset) — Kaggle

---

<div align="center">

**Built by [Sneha Timmavvagol](https://linkedin.com/in/sneha-timmavvagol)**

</div>
