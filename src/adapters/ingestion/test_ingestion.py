import pytest
from .datadog import DatadogAdapter
from models.canonical import CanonicalAlert

def test_datadog_normalize():
    adapter = DatadogAdapter()
    raw_alert = {
        "tags": {"service": "my-service"},
        "alert_type": "error",
        "title": "High CPU Usage",
        "body": "CPU usage is consistently above 90%",
        "hostname": "web-server-01",
        "some_other_field": "value"
    }

    canonical_alert = adapter.normalize(raw_alert)

    assert isinstance(canonical_alert, CanonicalAlert)
    assert canonical_alert.service_name == "my-service"
    assert canonical_alert.severity == "error"
    assert canonical_alert.title == "High CPU Usage"
    assert canonical_alert.description == "CPU usage is consistently above 90%"
    assert canonical_alert.entity == "web-server-01"
    assert canonical_alert.source_system == "datadog"
    assert canonical_alert.raw_payload == raw_alert

def test_datadog_normalize_missing_fields():
    adapter = DatadogAdapter()
    raw_alert = {
        "title": "Missing Fields Test"
    }

    canonical_alert = adapter.normalize(raw_alert)

    assert isinstance(canonical_alert, CanonicalAlert)
    assert canonical_alert.service_name == "unknown-service"
    assert canonical_alert.severity == "info"
    assert canonical_alert.title == "Missing Fields Test"
    assert canonical_alert.description == "No Description"
    assert canonical_alert.entity == "unknown-host"
    assert canonical_alert.source_system == "datadog"
    assert canonical_alert.raw_payload == raw_alert
