from typing import Dict, Any
from models.canonical import CanonicalAlert, AlertDetails
from .base import BaseIngestionAdapter

class UnifiedWebhookAdapter(BaseIngestionAdapter):
    def normalize(self, raw_alert: Dict[str, Any]) -> CanonicalAlert:
        # The raw_alert is already in the unified format.
        # We just need to parse it into the Pydantic model.
        details_data = raw_alert.pop("details", {})
        return CanonicalAlert(
            **raw_alert,
            details=AlertDetails(**details_data),
            raw_payload=raw_alert
        )