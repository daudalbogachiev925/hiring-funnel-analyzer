from sqlalchemy import Column, Integer, String, Float, DateTime, Index
from sqlalchemy.sql import func
from app.database import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True)
    external_id = Column(String, unique=True, nullable=False)
    source = Column(String, index=True)
    role = Column(String, index=True)
    experience_years = Column(Integer, default=0)
    skills_score = Column(Float, default=0.0)
    stage = Column(String, index=True)
    applied_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    offered = Column(Integer, default=0)
    hired = Column(Integer, default=0)

    __table_args__ = (
        Index("ix_candidates_stage_role", "stage", "role"),
    )
