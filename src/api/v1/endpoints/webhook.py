from fastapi import APIRouter, Request, HTTPException
from services.alert_service import AlertService
from adapters.ingestion.unified import UnifiedWebhookAdapter
from adapters.notification.slack import SlackAdapter
from services.graph_service import GraphService
from services.vector_db_service import VectorDBService
from core.config import DB_PATH, DB_COLLECTION_NAME

router = APIRouter()

vector_db_service = VectorDBService(db_path=DB_PATH, collection_name=DB_COLLECTION_NAME)
graph_service = GraphService(vector_db_service=vector_db_service)

alert_service = AlertService(
    ingestion_adapter=UnifiedWebhookAdapter(),
    notification_adapter=SlackAdapter(),
    graph_service=graph_service,
)

@router.post("/webhook")
async def receive_unified_webhook(request: Request):
    try:
        raw_alert = await request.json()
        alert_service.process_alert(raw_alert)
        return {"status": "success", "explanation_sent_to_slack": True}
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
