from typing import Dict, Any
from adapters.ingestion.base import BaseIngestionAdapter
from adapters.notification.base import BaseNotificationAdapter
from core.llm import get_explanation

class AlertService:
    def __init__(
        self,
        ingestion_adapter: BaseIngestionAdapter,
        notification_adapter: BaseNotificationAdapter,
    ):
        self.ingestion_adapter = ingestion_adapter
        self.notification_adapter = notification_adapter

    def process_alert(self, raw_alert: Dict[str, Any]):
        canonical_alert = self.ingestion_adapter.normalize(raw_alert)
        explanation = get_explanation(canonical_alert)
        print(explanation)
        self.notification_adapter.send(canonical_alert, explanation)
