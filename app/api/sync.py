from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.integrations.greenhouse import GreenhouseClient
from app.integrations.lever import LeverClient
from app.tasks.sync_candidates import sync_candidates_task

router = APIRouter()

@router.post("/{provider}")
def trigger_sync(provider: str, background: BackgroundTasks):
    if provider not in ("greenhouse", "lever"):
        raise HTTPException(400, "Unknown provider")
    background.add_task(sync_candidates_task.delay, provider)
    return {"status": "queued", "provider": provider}
