import os
from dotenv import load_dotenv
import openai
import requests
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any
from operator import inv
from operator import invert

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# Load configuration from environment variables
LLM_API_KEY = os.getenv("LLM_API_KEY")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
LLM_BASE_URL = os.getenv("LLM_BASE_URL")
LLM_MODEL= os.getenv("LLM_MODEL")

# Check if the environment variables are set
if not LLM_API_KEY:
    raise ValueError("LLM_API_KEY environment variable not set.")
if not SLACK_WEBHOOK_URL:
    raise ValueError("SLACK_WEBHOOK_URL environment variable not set.")
if not LLM_BASE_URL:
    raise ValueError("LLM_BASE_URL environment variable not set.")


# Initialize the OpenAI client
# Make sure to set the API key in your environment or pass it directly
# client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = openai.OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)


# --- Data Models (Using Pydantic for validation) ---

# This is our internal, standardized format. The adapter's job is to create this.
class CanonicalAlert(BaseModel):
    service_name: str
    severity: str
    title: str
    description: str
    entity: str
    metrics: Dict[str, Any] = Field(default_factory=dict)
    source_system: str
    raw_payload: Dict[str, Any] # Store the original alert for context


# --- FastAPI Application ---
app = FastAPI()

@app.post("/webhook/explain/datadog")
async def handle_datadog_webhook(request: Request):
    """
    Receives a webhook from Datadog, normalizes it, gets an explanation from an LLM,
    and sends it to Slack.
    """
    try:
        # 1. RECEIVE & NORMALIZE (This is your "Datadog Adapter")
        raw_alert = await request.json()

        # This parsing logic is specific to Datadog's webhook format.
        # You would write different logic for Grafana, CloudWatch, etc.
        canonical_alert = CanonicalAlert(
            service_name=raw_alert.get('tags', {}).get('service', 'unknown-service'),
            severity=raw_alert.get('alert_type', 'info'),
            title=raw_alert.get('title', 'No Title'),
            description=raw_alert.get('body', 'No Description'),
            entity=raw_alert.get('hostname', 'unknown-host'),
            source_system="datadog",
            raw_payload=raw_alert
        )

        # 2. EXPLAIN (The LLM Core)
        prompt = f"""
        You are an on-call engineering assistant with senior experience. Your job is to explain a technical monitoring alert for a notification channel.
        give a detailed report of the alert as possible by given data for user to understand as fast as possible. inspect and investigate the circumstances with given tools.
        You MUST given what you have investigated and what you have found.

        Here is the alert data in a structured format:
        - Service: {canonical_alert.service_name}
        - Severity: {canonical_alert.severity}
        - Title: {canonical_alert.title}
        - Description: {canonical_alert.description}
        - Affected Entity: {canonical_alert.entity}

        Based on this information, provide a structured report of what is happening.
        """

        response = client.chat.completions.create(
            model=LLM_MODEL, # or "gpt-4"
            messages=[
                {"role": "system", "content": "You are an on-call engineering assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )
        explanation = response.choices[0].message.content

        # 3. NOTIFY (The "Slack Adapter")
        slack_message = {
            "text": f"🚨 New Alert: {canonical_alert.title}",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f"🚨 {canonical_alert.title}"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f"*Service:*\n`{canonical_alert.service_name}`"},
                        {"type": "mrkdwn", "text": f"*Severity:*\n`{canonical_alert.severity.upper()}`"},
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
                            "text": f"Source: {canonical_alert.source_system}"
                        }
                    ]
                }
            ]
        }

        print(slack_message)

        # requests.post(SLACK_WEBHOOK_URL, json=slack_message)

        return {"status": "success", "explanation_sent_to_slack": True}

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# To run the app: uvicorn main:app --reload
