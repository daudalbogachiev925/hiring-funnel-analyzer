import argparse
from pathlib import Path
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUM_FEATURES = ["experience_years", "skills_score"]
CAT_FEATURES = ["source", "role", "stage"]

def build_pipeline() -> Pipeline:
    pre = ColumnTransformer([
        ("num", StandardScaler(), NUM_FEATURES),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CAT_FEATURES),
    ])
    return Pipeline([
        ("pre", pre),
        ("clf", GradientBoostingClassifier(
            n_estimators=300, learning_rate=0.05, max_depth=4, random_state=42)),
    ])

def train(df: pd.DataFrame, out_path: str) -> dict:
    df = df.dropna(subset=["offered"])
    X = df[NUM_FEATURES + CAT_FEATURES]
    y = df["offered"]

    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)

    pipe = build_pipeline()
    pipe.fit(X_tr, y_tr)
    proba = pipe.predict_proba(X_te)[:, 1]
    auc = roc_auc_score(y_te, proba)

    cv = cross_val_score(pipe, X, y, cv=5, scoring="roc_auc")
    pipe.fit(X, y)
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, out_path)

    return {"test_auc": float(auc), "cv_auc_mean": float(cv.mean()),
            "cv_auc_std": float(cv.std()), "n_samples": len(df)}

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--data", required=True)
    p.add_argument("--out", default="app/ml/model.pkl")
    args = p.parse_args()
    df = pd.read_csv(args.data)
    metrics = train(df, args.out)
    print(metrics)
