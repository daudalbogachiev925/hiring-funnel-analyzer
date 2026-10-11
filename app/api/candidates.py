from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Candidate
from app.schemas import CandidateCreate, CandidateRead

router = APIRouter()

@router.post("", response_model=CandidateRead, status_code=201)
def create_candidate(payload: CandidateCreate, db: Session = Depends(get_db)):
    existing = db.query(Candidate).filter(
        Candidate.external_id == payload.external_id).first()
    if existing:
        raise HTTPException(409, "external_id already exists")
    c = Candidate(**payload.model_dump())
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

@router.get("", response_model=List[CandidateRead])
def list_candidates(
    stage: Optional[str] = None,
    role: Optional[str] = None,
    limit: int = Query(100, le=1000),
    offset: int = 0,
    db: Session = Depends(get_db),
):
    q = db.query(Candidate)
    if stage:
        q = q.filter(Candidate.stage == stage)
    if role:
        q = q.filter(Candidate.role == role)
    return q.offset(offset).limit(limit).all()

@router.get("/{candidate_id}", response_model=CandidateRead)
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    c = db.query(Candidate).get(candidate_id)
    if not c:
        raise HTTPException(404, "Candidate not found")
    return c

@router.delete("/{candidate_id}", status_code=204)
def delete_candidate(candidate_id: int, db: Session = Depends(get_db)):
    c = db.query(Candidate).get(candidate_id)
    if not c:
        raise HTTPException(404, "Candidate not found")
    db.delete(c)
    db.commit()
