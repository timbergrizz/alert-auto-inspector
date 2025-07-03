from typing import Dict, Any
from adapters.ingestion.base import BaseIngestionAdapter
from adapters.notification.base import BaseNotificationAdapter
from core.llm import get_explanation
from services.vector_db_service import VectorDBService

class AlertService:
    def __init__(
        self,
        ingestion_adapter: BaseIngestionAdapter,
        notification_adapter: BaseNotificationAdapter,
        vector_db_service: VectorDBService,
    ):
        self.ingestion_adapter = ingestion_adapter
        self.notification_adapter = notification_adapter
        self.vector_db_service = vector_db_service
        self.vector_db_service.get_or_create_collection("knowledge_base")

    def process_alert(self, raw_alert: Dict[str, Any]):
        canonical_alert = self.ingestion_adapter.normalize(raw_alert)
        
        # Query vector DB for relevant context
        query_text = f"{canonical_alert.title} {canonical_alert.service}"
        context_results = self.vector_db_service.query_documents(query_texts=[query_text])
        
        # Extract relevant documents from the query results
        context_documents = context_results.get('documents', [[]])[0]
        
        explanation = get_explanation(canonical_alert, context_documents)
        print(explanation)
        self.notification_adapter.send(canonical_alert, explanation)
