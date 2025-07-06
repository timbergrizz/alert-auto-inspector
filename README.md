# Alert Explainer

## Overview

This project, "Alert Explainer," aims to develop a universal observability automation platform. Its primary goal is to ingest alerts from any monitoring source, use a Large Language Model (LLM) to investigate the circumstances, and provide human-readable analysis and actionable remediation steps to on-call engineers. The core principles are decoupling, standardization, and extensibility through a pluggable, adapter-based design.

## The Problem: Disparate Monitoring Alerts

Modern IT environments use various monitoring tools (Datadog, Grafana, New Relic, Sentry, etc.), each generating alerts with unique and often non-standardized JSON payloads. This leads to:

-   **Non-standardized Payloads:** Each tool has its own unique alert structure.
-   **Configuration Dependency:** Payload structures can vary even within the same tool based on alert type and user configuration.
-   **Scalability Limitations:** Integrating new monitoring tools requires code changes and redeployment, increasing maintenance overhead.

## The Solution: Standardized Webhook Integration

Instead of the receiving end adapting to every format, this solution enforces that the sending end (monitoring tool) sends data in a single, predefined **Unified Alert Format**. This is achieved by leveraging custom payload/template features available in most monitoring systems.

### High-Level Architecture

The system processes an alert from ingestion to notification through several logical layers:

1.  **Ingestion Layer:** Receives raw JSON payloads via a Universal Webhook Endpoint and converts them into a Canonical Alert Format using an Alert Normalizer/Adapter.
2.  **Core Engine:** Orchestrates the workflow, including an LLM Investigation Agent that queries a State & Knowledge DB (VectorDB + SQL/NoSQL) for context.
3.  **Data Abstraction Layer:** Provides the LLM with "tools" to query various data sources via Data Fetching Adapters.
4.  **Action Layer:** Handles notifications and other actions via Notification/Action Adapters.

### Canonical Alert Format

The standardized JSON format for incoming alerts:

```json
{
  "title": "String, /* Clear title of the alert (e.g., 'Auth-API CPU usage critical') */",
  "environment": "String, /* Environment where the incident occurred (e.g., 'production', 'staging') */",
  "service": "String, /* Name of the service/application affected */",
  "severity": "String, /* Severity level ('Critical', 'Warning', 'Info') */",
  "status": "String, /* Alert status ('firing', 'resolved') */",
  "timestamp": "String, /* Occurrence time (ISO 8601 format) */",
  "details": {
    "metric": "String, /* Metric measured (e.g., 'CPUUtilization') */",
    "current_value": "String, /* Current value */",
    "threshold": "String, /* Threshold value */",
    "condition": "String, /* Condition (e.g., 'persisting for 5 minutes') */"
  },
  "link_to_source": "String (URL), /* Link to the original alert in the monitoring tool (Deep Link) */",
  "runbook_url": "String (URL), /* Link to the incident response guide (Optional) */",
  "owner_team": "String, /* Responsible team/person (Optional) */",
  "tags": {
    "Key": "Value" /* Additional metadata for filtering and routing (Optional) */
  },
  "image_url": "String (URL), /* URL of a graph image at the time of the alert (Optional) */"
}
```

### API Endpoint

The system exposes a single webhook endpoint to receive standardized alerts.

**Endpoint:** `POST /api/v1/webhook/webhook`
**Content-Type:** `application/json`

**Example Request:**

```bash
curl -X POST \
  http://localhost:8000/api/v1/webhook/webhook \
  -H 'Content-Type: application/json' \
  -d '{
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
  }'
```

## Milestones / Roadmap

This project follows a phased implementation plan:

1.  **Alert Explainer (MVP):** Prove the core concept with a single webhook endpoint, hardcoded adapter, stateless LLM call for explanation, and single notification destination (e.g., Slack).
2.  **Contextualizer:** Introduce a Vector Database and implement Retrieval-Augmented Generation (RAG) for semantic search of alert details, populating it with runbooks, post-mortems, etc.
3.  **Junior Investigator:** Enable the LLM to actively fetch more information using a ReAct (Reason + Act) loop and data abstraction layer with "tools."
4.  **Universal Adaptor Platform:** Refactor adapters for ingestion and data-fetching into pluggable modules, making the system universal and production-ready.
5.  **Autonomous SRE:** (Future) Enable closed-loop remediation with secure "write" tools and human-in-the-loop approval workflows.

## Getting Started (Placeholder)

This project is built with Python and FastAPI. More detailed setup instructions will be provided here.

## Testing

This project uses `pytest` for testing. To run all tests, navigate to the project's root directory and execute:

```bash
uv run pytest
```

For more details on writing and running tests, refer to `doc/test.md`.