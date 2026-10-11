from functools import lru_cache
import joblib
import numpy as np
import pandas as pd
import shap
from app.config import settings

@lru_cache(maxsize=1)
def _load_model():
    return joblib.load(settings.MODEL_PATH)

def explain(df: pd.DataFrame) -> dict:
    pipe = _load_model()
    pre = pipe.named_steps["pre"]
    clf = pipe.named_steps["clf"]
    X_trans = pre.transform(df)
    feature_names = pre.get_feature_names_out()
    explainer = shap.TreeExplainer(clf)
    shap_values = explainer.shap_values(X_trans)
    if isinstance(shap_values, list):
        shap_values = shap_values[1]
    values = shap_values[0]
    pairs = sorted(
        zip(feature_names, values.tolist()),
        key=lambda x: abs(x[1]), reverse=True
    )[:10]
    return {
        "base_value": float(explainer.expected_value if np.isscalar(explainer.expected_value)
                            else explainer.expected_value[1]),
        "top_features": [{"feature": f, "impact": round(v, 4)} for f, v in pairs],
    }
