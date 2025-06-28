from pydantic import BaseModel, Field
from typing import Dict, Any

class CanonicalAlert(BaseModel):
    service_name: str
    severity: str
    title: str
    description: str
    entity: str
    metrics: Dict[str, Any] = Field(default_factory=dict)
    source_system: str
    raw_payload: Dict[str, Any] # Store the original alert for context
