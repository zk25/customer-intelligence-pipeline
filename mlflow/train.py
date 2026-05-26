import mlflow
import mlflow.xgboost
import pandas as pd
import xgboost as xgb
import shap
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, classification_report

# Load RFM features from PySpark output
rfm = pd.read_parquet("data/processed/rfm_features")
print(f"Loaded {len(rfm)} rows")

# Create churn label: churned if recency > 180 days
rfm["churned"] = (rfm["recency"] > 180).astype(int)
print(f"Churn rate: {rfm['churned'].mean():.1%}")

X = rfm[["recency", "frequency", "monetary"]]
y = rfm["churned"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Connect to MLflow
mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("churn_prediction")

with mlflow.start_run(run_name="xgboost_v1"):
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        random_state=42,
        eval_metric="logloss"
    )
    model.fit(X_train, y_train)

    preds = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, preds)
    print(f"\nAUC-ROC: {auc:.3f}")

    # Log to MLflow
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 4)
    mlflow.log_metric("auc_roc", round(auc, 3))
    mlflow.xgboost.log_model(model, "xgboost_model")

    # SHAP plot
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)
    shap.summary_plot(shap_values, X_test, show=False)
    plt.tight_layout()
    plt.savefig("dashboards/screenshots/shap_summary.png")
    plt.close()
    mlflow.log_artifact("dashboards/screenshots/shap_summary.png")

    print(f"\nRun logged to MLflow at http://localhost:5000")
    print("Open MLflow UI → Experiments → churn_prediction to see results")