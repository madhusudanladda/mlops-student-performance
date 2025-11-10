
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi.responses import PlainTextResponse
import joblib, os

app = FastAPI(title="Student Performance API")
model = joblib.load("/app/models/model.pkl") if os.path.exists("/app/models/model.pkl") else None

PREDICTIONS = Counter("sp_predictions_total", "Total predictions")
ERRORS = Counter("sp_errors_total", "Total errors")
LATENCY = Histogram("sp_prediction_latency_seconds", "Prediction latency")
MODEL_VERSION = Gauge("sp_model_version_info", "Model version", ["stage", "version"])
MODEL_VERSION.labels(stage="Production", version="v1").set(1)

class Item(BaseModel):
    features: dict

@app.get("/")
def root():
    return {"status": "ok", "model_loaded": model is not None}

@app.post("/predict")
@LATENCY.time()
def predict(item: Item):
    try:
        X = pd.DataFrame([item.features])
        y = model.predict(X)[0]
        PREDICTIONS.inc()
        return {"prediction": int(y) if hasattr(y, "item") else y}
    except Exception as e:
        ERRORS.inc()
        return {"error": str(e)}

@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return generate_latest()
