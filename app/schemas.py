from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class CandidateBase(BaseModel):
    external_id: str
    source: str
    role: str
    experience_years: int = Field(ge=0, le=60)
    skills_score: float = Field(ge=0, le=100)
    stage: str

class CandidateCreate(CandidateBase):
    offered: int = 0
    hired: int = 0

class CandidateRead(CandidateBase):
    id: int
    offered: int
    hired: int
    applied_at: Optional[datetime]

    class Config:
        from_attributes = True

class PredictionRead(BaseModel):
    candidate_id: int
    offer_probability: float
    explanation: dict

class FunnelStage(BaseModel):
    stage: str
    count: int
    conversion_to_next: float
