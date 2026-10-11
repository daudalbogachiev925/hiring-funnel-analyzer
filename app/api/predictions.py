from functools import lru_cache
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import joblib
from app.config import settings
from app.database import get_db
from app.models import Candidate
from app.ml.explain import explain
from app.ml.features import candidate_to_frame
from app.schemas import PredictionRead

router = APIRouter()

@lru_cache(maxsize=1)
def _model():
    return joblib.load(settings.MODEL_PATH)

@router.get("/{candidate_id}", response_model=PredictionRead)
def predict(candidate_id: int, db: Session = Depends(get_db)):
    c = db.query(Candidate).get(candidate_id)
    if not c:
        raise HTTPException(404, "Candidate not found")
    df = candidate_to_frame(c)
    try:
        proba = float(_model().predict_proba(df)[0, 1])
    except FileNotFoundError:
        raise HTTPException(503, "Model not trained")
    return PredictionRead(
        candidate_id=candidate_id,
        offer_probability=round(proba, 4),
        explanation=explain(df),
    )

@router.post("/batch")
def predict_batch(candidate_ids: list[int], db: Session = Depends(get_db)):
    cands = db.query(Candidate).filter(Candidate.id.in_(candidate_ids)).all()
    if not cands:
        raise HTTPException(404, "No candidates")
    df = candidate_to_frame(cands[0])
    for c in cands[1:]:
        df = df.append(candidate_to_frame(c), ignore_index=True)
    probas = _model().predict_proba(df)[:, 1]
    return [{"candidate_id": c.id, "offer_probability": float(p)}
            for c, p in zip(cands, probas)]
