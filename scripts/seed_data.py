import random
from app.database import SessionLocal
from app.models import Candidate

STAGES = ["applied", "screen", "tech", "onsite", "offer", "hired"]
ROLES = ["backend", "frontend", "data", "devops", "qa"]
SOURCES = ["linkedin", "referral", "career_page", "agency"]

def seed(n: int = 500):
    db = SessionLocal()
    try:
        for i in range(n):
            stage = random.choice(STAGES)
            c = Candidate(
                external_id=f"seed_{i}",
                source=random.choice(SOURCES),
                role=random.choice(ROLES),
                experience_years=random.randint(0, 20),
                skills_score=random.uniform(20, 100),
                stage=stage,
                offered=1 if stage in ("offer", "hired") else 0,
                hired=1 if stage == "hired" else 0,
            )
            db.add(c)
        db.commit()
        print(f"Seeded {n} candidates")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
