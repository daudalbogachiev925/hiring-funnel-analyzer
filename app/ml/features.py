import pandas as pd
from sqlalchemy.orm import Session
from app.models import Candidate

FEATURE_COLUMNS = ["experience_years", "skills_score", "source", "role", "stage"]

def build_features(db: Session) -> pd.DataFrame:
    rows = db.query(Candidate).all()
    return pd.DataFrame([{
        "experience_years": c.experience_years,
        "skills_score": c.skills_score,
        "source": c.source,
        "role": c.role,
        "stage": c.stage,
        "offered": c.offered,
    } for c in rows])

def candidate_to_frame(candidate: Candidate) -> pd.DataFrame:
    return pd.DataFrame([{
        "experience_years": candidate.experience_years,
        "skills_score": candidate.skills_score,
        "source": candidate.source,
        "role": candidate.role,
        "stage": candidate.stage,
    }])
