from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.database import get_db
from app.models import Candidate
from app.schemas import FunnelStage

router = APIRouter()

STAGE_ORDER = ["applied", "screen", "tech", "onsite", "offer", "hired"]

@router.get("/funnel", response_model=List[FunnelStage])
def funnel(db: Session = Depends(get_db)):
    rows = db.query(Candidate.stage, func.count(Candidate.id)) \
             .group_by(Candidate.stage).all()
    counts = {stage: count for stage, count in rows}
    ordered = [(s, counts.get(s, 0)) for s in STAGE_ORDER]
    result = []
    for i, (stage, count) in enumerate(ordered):
        next_count = ordered[i+1][1] if i+1 < len(ordered) else count
        conv = (next_count / count) if count else 0.0
        result.append(FunnelStage(stage=stage, count=count,
                                  conversion_to_next=round(conv, 3)))
    return result

@router.get("/sources")
def sources_breakdown(db: Session = Depends(get_db)):
    rows = db.query(Candidate.source, func.count(Candidate.id)) \
             .group_by(Candidate.source).all()
    return [{"source": s, "count": c} for s, c in rows]
