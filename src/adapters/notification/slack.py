import requests
from core.config import SLACK_WEBHOOK_URL
from models.canonical import CanonicalAlert
from .base import BaseNotificationAdapter

class SlackAdapter(BaseNotificationAdapter):
    def send(self, alert: CanonicalAlert, explanation: str):
        slack_message = {
            "text": "🚨 New Alert: {alert.title}",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "🚨 {alert.title}"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": "*Service:*\n`{alert.service_name}`"},
                        {"type": "mrkdwn", "text": "*Severity:*\n`{alert.severity.upper()}`"},
                    ]
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*What's Happening (Explained by AI):*\n{explanation}"
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": "Source: {alert.source_system}"
                        }
                    ]
                }
            ]
        }
        requests.post(SLACK_WEBHOOK_URL, json=slack_message)
