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
