
import joblib, pandas as pd

_model = None
def load_model(path="models/model.pkl"):
    global _model
    if _model is None:
        _model = joblib.load(path)
    return _model

def predict(records: list[dict]):
    model = load_model()
    X = pd.DataFrame.from_records(records)
    return model.predict(X).tolist()
