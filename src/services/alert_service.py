from typing import Dict, Any
from adapters.ingestion.base import BaseIngestionAdapter
from adapters.notification.base import BaseNotificationAdapter
from services.graph_service import GraphService

class AlertService:
    def __init__(
        self,
        ingestion_adapter: BaseIngestionAdapter,
        notification_adapter: BaseNotificationAdapter,
        graph_service: GraphService,
    ):
        self.ingestion_adapter = ingestion_adapter
        self.notification_adapter = notification_adapter
        self.graph_service = graph_service

    def process_alert(self, raw_alert: Dict[str, Any]):
        canonical_alert = self.ingestion_adapter.normalize(raw_alert)
        
        explanation = self.graph_service.run(canonical_alert)
        
        print(explanation)
        self.notification_adapter.send(canonical_alert, explanation)
