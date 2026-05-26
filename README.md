# Customer Intelligence Pipeline

## Live Dashboard
[View Tableau Dashboard](https://public.tableau.com/app/profile/zainab.khan4210/viz/CustomerIntelligenceDashboard/Dashboard3)

## Problem Statement
E-commerce businesses lose revenue due to customer churn and poor segment targeting. This pipeline transforms 93K+ raw order records into actionable customer segments, churn predictions, and live KPI dashboards.

## Tech Stack
| Layer | Tools |
|-------|-------|
| Cloud Storage | AWS S3, AWS Glue, Glue Data Catalog |
| Processing | PySpark 3.5 (93K rows, RFM features) |
| Transformation | dbt (10 models, 3-layer architecture) |
| Orchestration | Apache Airflow (5-task DAG, weekly schedule) |
| ML Tracking | MLflow (XGBoost, AUC 1.0, SHAP explainability) |
| Containerisation | Docker Compose (3 services) |
| CI/CD | GitHub Actions |
| Visualisation | Tableau Public (4-page live dashboard) |

## Key Findings
- High-value customers (top 7%) drive significant revenue concentration
- 59% of customers are churned (recency > 180 days)
- Low-value segment dominates at 62% of total customers

## How to Run
git clone https://github.com/zk25/customer-intelligence-pipeline
cd customer-intelligence-pipeline
docker compose up -d
source venv/bin/activate
python spark/eda.py
python mlflow/train.py
