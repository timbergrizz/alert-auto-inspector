from fastapi import APIRouter, Request, HTTPException
from services.alert_service import AlertService
from adapters.ingestion.datadog import DatadogAdapter
from adapters.notification.slack import SlackAdapter

router = APIRouter()

alert_service = AlertService(
    ingestion_adapter=DatadogAdapter(),
    notification_adapter=SlackAdapter(),
)

@router.post("/explain/datadog")
async def handle_datadog_webhook(request: Request):
    try:
        raw_alert = await request.json()
        alert_service.process_alert(raw_alert)
        return {"status": "success", "explanation_sent_to_slack": True}
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
