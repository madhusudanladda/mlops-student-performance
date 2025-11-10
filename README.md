
# MLOps Student Performance (End-to-End Template)

A production-style template that satisfies your problem statement:
- Model versioning (DVC + MLflow Registry)
- Auto-deploy via CI/CD (GitHub Actions)
- Monitoring (Prometheus, Grafana) + Alerts (Alertmanager/Slack)
- Collaborative Git workflow

## Quickstart (Local, Docker Compose)

```bash
# 0) Prereqs: Docker + Docker Compose, Git, Python 3.11
# 1) Create venv & install deps
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2) Initialize DVC & add remote (edit to your choice)
dvc init
# Example with local remote
dvc remote add -d storage ./dvcstore

# 3) Put your dataset at data/raw/StudentsPerformance.csv
# or run the synthetic generator:
python -m src.data.make_dataset --output data/raw/StudentsPerformance.csv

# 4) Reproduce pipeline (process -> train -> evaluate)
dvc repro

# 5) Bring up local stack (API + MLflow + Prometheus + Grafana)
docker compose up -d
# API:       http://localhost:8000
# MLflow:    http://localhost:5000
# Prometheus http://localhost:9090
# Grafana:   http://localhost:3000 (user: admin / pass: admin)

# 6) Test prediction
curl -X POST http://localhost:8000/predict -H 'Content-Type: application/json'   -d '{"features":{"gender":"female","race/ethnicity":"group B","parental level of education":"bachelor's degree","lunch":"standard","test preparation course":"completed","reading score":80,"writing score":82}}'
```

## CI/CD
- On push to `main`, CI: tests + DVC pipeline + log to MLflow + build image.
- CD: pushes image and (example) redeploys via Docker on a remote host (can switch to Kubernetes).

## Monitoring & Alerts
- `/metrics` exposed by API for Prometheus.
- Grafana dashboard JSON included under `conf/grafana` (placeholder).
