from abc import ABC, abstractmethod
from typing import Dict, Any
from models.canonical import CanonicalAlert

class BaseIngestionAdapter(ABC):
    @abstractmethod
    def normalize(self, raw_data: Dict[str, Any]) -> CanonicalAlert:
        pass
