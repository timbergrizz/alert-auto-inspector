from unittest.mock import MagicMock, patch

from pydantic.networks import HttpUrl
from models.canonical import AlertDetails, CanonicalAlert
from services.alert_service import AlertService


def test_process_alert():
    # Arrange
    mock_ingestion_adapter = MagicMock()
    mock_notification_adapter = MagicMock()
    mock_graph_service = MagicMock()

    raw_alert = {"title": "Test Alert"}
    canonical_alert = CanonicalAlert(
        title="Test Alert",
        environment="test",
        service="test-service",
        severity="critical",
        status="firing",
        timestamp="2025-07-03T12:00:00Z",
        details=AlertDetails(metric="test"),
        link_to_source=HttpUrl("http://example.com/source"),
        raw_payload=raw_alert
    )
    explanation = "This is a test explanation."

    mock_ingestion_adapter.normalize.return_value = canonical_alert
    mock_graph_service.run.return_value = explanation

    alert_service = AlertService(
        ingestion_adapter=mock_ingestion_adapter,
        notification_adapter=mock_notification_adapter,
        graph_service=mock_graph_service,
    )

    # Act
    alert_service.process_alert(raw_alert)

    # Assert
    mock_ingestion_adapter.normalize.assert_called_once_with(raw_alert)
    mock_graph_service.run.assert_called_once_with(canonical_alert)
    mock_notification_adapter.send.assert_called_once_with(canonical_alert, explanation)