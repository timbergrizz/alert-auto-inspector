import requests
from core.config import SLACK_WEBHOOK_URL
from models.canonical import CanonicalAlert
from .base import BaseNotificationAdapter

class SlackAdapter(BaseNotificationAdapter):
    def send(self, alert: CanonicalAlert, explanation: str):
        slack_message = {
            "text": f"🚨 New Alert: {alert.title}",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"🚨 {alert.title}"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f"*Service:*\n`{alert.service_name}`"},
                        {"type": "mrkdwn", "text": f"*Severity:*\n`{alert.severity.upper()}`"},
                    ]
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*What's Happening (Explained by AI):*\n{explanation}"
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": f"Source: {alert.source_system}"
                        }
                    ]
                }
            ]
        }
        requests.post(SLACK_WEBHOOK_URL, json=slack_message)
