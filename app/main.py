from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import candidates, stages, predictions, sync
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hiring Funnel Analyzer", version="1.0.0")

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(candidates.router, prefix="/api/candidates", tags=["candidates"])
app.include_router(stages.router, prefix="/api/stages", tags=["stages"])
app.include_router(predictions.router, prefix="/api/predictions", tags=["predictions"])
app.include_router(sync.router, prefix="/api/sync", tags=["sync"])

@app.get("/health")
def health():
    return {"status": "ok", "service": "hiring-funnel-analyzer"}
