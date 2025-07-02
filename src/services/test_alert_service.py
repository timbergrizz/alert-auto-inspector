from unittest.mock import MagicMock, patch
from models.canonical import CanonicalAlert
from services.alert_service import AlertService


@patch('services.alert_service.get_explanation')
def test_process_alert(mock_get_explanation):
    # Arrange
    mock_ingestion_adapter = MagicMock()
    mock_notification_adapter = MagicMock()

    raw_alert = {"title": "Test Alert"}
    canonical_alert = CanonicalAlert(
        service_name="test-service",
        severity="critical",
        title="Test Alert",
        description="This is a test alert.",
        entity="test-entity",
        source_system="test-system",
        raw_payload=raw_alert
    )
    explanation = "This is a test explanation."

    mock_ingestion_adapter.normalize.return_value = canonical_alert
    mock_get_explanation.return_value = explanation

    alert_service = AlertService(
        ingestion_adapter=mock_ingestion_adapter,
        notification_adapter=mock_notification_adapter,
    )

    # Act
    alert_service.process_alert(raw_alert)

    # Assert
    mock_ingestion_adapter.normalize.assert_called_once_with(raw_alert)
    mock_get_explanation.assert_called_once_with(canonical_alert)
    mock_notification_adapter.send.assert_called_once_with(canonical_alert, explanation)
