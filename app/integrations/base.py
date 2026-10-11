from abc import ABC, abstractmethod
from typing import List, Dict

class ATSClient(ABC):
    @abstractmethod
    def fetch_candidates(self) -> List[Dict]:
        ...

    @abstractmethod
    def fetch_stages(self) -> Dict[str, str]:
        ...
