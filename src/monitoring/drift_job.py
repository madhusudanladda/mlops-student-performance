
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
from evidently.report import Report
from evidently.metrics import DataDriftPreset
import pandas as pd

# Reference: training features
ref = pd.read_csv('data/processed/features.csv').sample(500, replace=True)
# Current: pretend last-batch production data
# In a real system, read from logs or DB
curr = ref.sample(300, replace=True)

report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=ref, current_data=curr)
summary = report.as_dict()
score = float(summary['metrics'][0]['result']['dataset_drift']['drift_share'])

reg = CollectorRegistry()
DRIFT = Gauge('sp_drift_share', 'Share of drifting features', registry=reg)
DRIFT.set(score)
push_to_gateway('pushgateway:9091', job='drift', registry=reg)
print("✅ Drift pushed:", score)
