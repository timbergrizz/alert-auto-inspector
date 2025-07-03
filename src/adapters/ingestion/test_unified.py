import pytest
from .unified import UnifiedWebhookAdapter
from models.canonical import CanonicalAlert, AlertDetails

def test_unified_webhook_normalize():
    adapter = UnifiedWebhookAdapter()
    raw_alert = {
        "title": "Auth-API CPU usage critical",
        "environment": "production",
        "service": "auth-api",
        "severity": "Critical",
        "status": "firing",
        "timestamp": "2025-07-03T10:00:00Z",
        "details": {
            "metric": "CPUUtilization",
            "current_value": "95%",
            "threshold": "90%",
            "condition": "5m"
        },
        "link_to_source": "http://my-grafana.com/d/abcdefg/my-dashboard?orgId=1&viewPanel=2",
        "runbook_url": "http://my-runbook.com/cpu-usage",
        "owner_team": "backend-dev",
        "tags": {
            "region": "us-east-1"
        },
        "image_url": "http://my-grafana.com/render/d-solo/abcdefg/my-dashboard?orgId=1&panelId=2"
    }

    canonical_alert = adapter.normalize(raw_alert)

    assert isinstance(canonical_alert, CanonicalAlert)
    assert canonical_alert.title == "Auth-API CPU usage critical"
    assert canonical_alert.environment == "production"
    assert canonical_alert.service == "auth-api"
    assert canonical_alert.severity == "Critical"
    assert canonical_alert.status == "firing"
    assert canonical_alert.timestamp == "2025-07-03T10:00:00Z"
    assert isinstance(canonical_alert.details, AlertDetails)
    assert canonical_alert.details.metric == "CPUUtilization"
    assert str(canonical_alert.link_to_source) == "http://my-grafana.com/d/abcdefg/my-dashboard?orgId=1&viewPanel=2"
    assert canonical_alert.raw_payload == raw_alert

def test_unified_webhook_normalize_minimal():
    adapter = UnifiedWebhookAdapter()
    raw_alert = {
        "title": "Minimal Alert",
        "environment": "staging",
        "service": "test-service",
        "severity": "Info",
        "status": "resolved",
        "timestamp": "2025-07-03T11:00:00Z",
        "details": {},
        "link_to_source": "http://example.com/alert"
    }

    canonical_alert = adapter.normalize(raw_alert)

    assert isinstance(canonical_alert, CanonicalAlert)
    assert canonical_alert.title == "Minimal Alert"
    assert canonical_alert.environment == "staging"
    assert canonical_alert.service == "test-service"
    assert canonical_alert.severity == "Info"
    assert canonical_alert.status == "resolved"
    assert canonical_alert.details.metric is None
    assert canonical_alert.runbook_url is None
    assert canonical_alert.owner_team is None
    assert canonical_alert.tags == {}
    assert canonical_alert.image_url is None
    assert canonical_alert.raw_payload == raw_alert