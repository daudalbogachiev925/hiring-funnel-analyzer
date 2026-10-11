from app.worker import celery
from app.database import SessionLocal
from app.models import Candidate
from app.integrations.greenhouse import GreenhouseClient
from app.integrations.lever import LeverClient

@celery.task(name="sync_candidates")
def sync_candidates_task(provider: str):
    db = SessionLocal()
    try:
        client = GreenhouseClient() if provider == "greenhouse" else LeverClient()
        items = client.fetch_candidates()
        inserted = 0
        for item in items:
            existing = db.query(Candidate).filter(
                Candidate.external_id == item["external_id"]).first()
            if existing:
                for k, v in item.items():
                    setattr(existing, k, v)
            else:
                db.add(Candidate(**item))
                inserted += 1
        db.commit()
        return {"provider": provider, "total": len(items), "inserted": inserted}
    finally:
        db.close()
