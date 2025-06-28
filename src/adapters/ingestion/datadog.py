from typing import Dict, Any
from models.canonical import CanonicalAlert
from .base import BaseIngestionAdapter

class DatadogAdapter(BaseIngestionAdapter):
    def normalize(self, raw_alert: Dict[str, Any]) -> CanonicalAlert:
        return CanonicalAlert(
            service_name=raw_alert.get('tags', {}).get('service', 'unknown-service'),
            severity=raw_alert.get('alert_type', 'info'),
            title=raw_alert.get('title', 'No Title'),
            description=raw_alert.get('body', 'No Description'),
            entity=raw_alert.get('hostname', 'unknown-host'),
            source_system="datadog",
            raw_payload=raw_alert
        )
