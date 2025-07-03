import pytest
from unittest.mock import patch, MagicMock
from .slack import SlackAdapter
from models.canonical import CanonicalAlert

@patch('requests.post')
def test_slack_send(mock_post):
    adapter = SlackAdapter()
    alert = CanonicalAlert(
        service="test-service",
        severity="critical",
        title="Test Alert",
        description="This is a test alert.",
        entity="test-entity",
        environment="test",
        status="firing",
        timestamp="2025-07-03T12:00:00Z",
        source_system="test-system",
        details={},
        link_to_source="http://example.com/source",
        raw_payload={"data": "test"}
    )
    explanation = "This is an explanation."

    adapter.send(alert, explanation)

    mock_post.assert_called_once()

    args, kwargs = mock_post.call_args

    assert 'json' in kwargs
    slack_message = kwargs['json']

    assert slack_message['text'] == f"🚨 New Alert: {alert.title}"
    assert slack_message['blocks'][0]['text']['text'] == f"🚨 {alert.title}"
    assert slack_message['blocks'][1]['fields'][0]['text'] == f"*Service:*\n`{alert.service}`"
    assert slack_message['blocks'][1]['fields'][1]['text'] == f"*Severity:*\n`{alert.severity.upper()}`"
    assert slack_message['blocks'][3]['text']['text'] == f"*What's Happening (Explained by AI):*\n{explanation}"
