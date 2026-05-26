import pandas as pd

# Load RFM features from PySpark output
rfm = pd.read_parquet('data/processed/rfm_features')

# Add segment column
rfm['segment'] = pd.cut(
    rfm['monetary'],
    bins=[0, 100, 300, 999999],
    labels=['Low Value', 'Mid Value', 'High Value']
)

# Add churn label
rfm['churned'] = (rfm['recency'] > 180).astype(int)

rfm.to_csv('data/dashboard_data.csv', index=False)
print(f'Exported {len(rfm)} rows to data/dashboard_data.csv')
print(rfm.head())
print(rfm['segment'].value_counts())
