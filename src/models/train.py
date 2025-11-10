
import argparse, json, yaml, os
import pandas as pd
import mlflow
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, accuracy_score
import joblib

def train(params_path: str):
    params = yaml.safe_load(open(params_path))
    df = pd.read_csv("data/processed/features.csv")
    y = (df["math score"] >= 70).astype(int) if params["problem_type"]=="classification" else df["math score"]
    X = df.drop(columns=["math score"])

    pre = ColumnTransformer([
        ("num", StandardScaler(), params["features"]["numeric"]),
        ("cat", OneHotEncoder(handle_unknown="ignore"), params["features"]["categorical"]),
    ])

    if params["model"]["name"] == "LogisticRegression":
        model = LogisticRegression(**params["model"]["params"])
    else:
        raise ValueError("Unsupported model for template")

    pipe = Pipeline([("pre", pre), ("model", model)])
    pipe.fit(X, y)

    preds = pipe.predict(X)
    metrics = {}
    if params["problem_type"]=="classification":
        metrics["accuracy"] = float(accuracy_score(y, preds))
        metrics["f1"] = float(f1_score(y, preds))
    else:
        # regression metrics placeholder
        pass

    os.makedirs("models", exist_ok=True)
    joblib.dump(pipe, "models/model.pkl")
    json.dump(metrics, open("metrics.json", "w"))
    print("✅ Metrics:", metrics)

    # MLflow logging
    mlflow.set_tracking_uri(params["mlflow"]["tracking_uri"])
    mlflow.set_experiment(params["mlflow"]["experiment"])
    with mlflow.start_run():
        mlflow.log_params(params["model"]["params"])
        mlflow.log_metrics(metrics)
        mlflow.sklearn.log_model(pipe, "model", registered_model_name=params["mlflow"]["registered_model_name"])

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--params", required=True)
    args = ap.parse_args()
    train(args.params)
