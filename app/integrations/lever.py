import httpx
from typing import List, Dict
from app.config import settings
from app.integrations.base import ATSClient

class LeverClient(ATSClient):
    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key or settings.LEVER_API_KEY
        self.base_url = base_url or settings.LEVER_BASE_URL

    def _auth(self):
        return (self.api_key, "")

    def fetch_candidates(self) -> List[Dict]:
        r = httpx.get(f"{self.base_url}/opportunities",
                      auth=self._auth(), timeout=30)
        r.raise_for_status()
        data = r.json().get("data", [])
        return [self._normalize(c) for c in data]

    def _normalize(self, c: dict) -> Dict:
        return {
            "external_id": f"lever_{c.get('id')}",
            "source": c.get("sources", ["unknown"])[0] if c.get("sources") else "unknown",
            "role": c.get("postings", [{}])[0].get("text", "unknown"),
            "experience_years": 0,
            "skills_score": 0.0,
            "stage": c.get("stage", "applied"),
        }

    def fetch_stages(self) -> Dict[str, str]:
        return {}
