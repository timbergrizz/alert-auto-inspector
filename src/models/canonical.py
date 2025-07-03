from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, Dict, Any

class AlertDetails(BaseModel):
    metric: Optional[str] = None
    current_value: Optional[str] = None
    threshold: Optional[str] = None
    condition: Optional[str] = None

class CanonicalAlert(BaseModel):
    title: str
    environment: str
    service: str
    severity: str
    status: str
    timestamp: str
    details: AlertDetails
    link_to_source: HttpUrl
    runbook_url: Optional[HttpUrl] = None
    owner_team: Optional[str] = None
    source_system: Optional[str] = None
    tags: Optional[Dict[str, str]] = {}
    image_url: Optional[HttpUrl] = None
    raw_payload: Dict[str, Any] # Store the original alert for context
