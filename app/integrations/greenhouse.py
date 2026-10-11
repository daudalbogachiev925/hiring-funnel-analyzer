import httpx
from typing import List, Dict
from app.config import settings
from app.integrations.base import ATSClient

class GreenhouseClient(ATSClient):
    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key or settings.GREENHOUSE_API_KEY
        self.base_url = base_url or settings.GREENHOUSE_BASE_URL

    def _headers(self):
        return {"Authorization": f"Basic {self.api_key}"}

    def fetch_candidates(self) -> List[Dict]:
        results = []
        page = 1
        while True:
            r = httpx.get(f"{self.base_url}/candidates",
                          params={"per_page": 100, "page": page},
                          headers=self._headers(), timeout=30)
            r.raise_for_status()
            data = r.json()
            if not data:
                break
            for c in data:
                results.append(self._normalize(c))
            page += 1
        return results

    def _normalize(self, c: dict) -> Dict:
        return {
            "external_id": f"gh_{c.get('id')}",
            "source": (c.get("sources") or [{}])[0].get("public_name", "unknown"),
            "role": (c.get("applications") or [{}])[0].get("jobs", [{}])[0].get("name", "unknown"),
            "experience_years": 0,
            "skills_score": 0.0,
            "stage": c.get("status", "applied"),
        }

    def fetch_stages(self) -> Dict[str, str]:
        return {}
