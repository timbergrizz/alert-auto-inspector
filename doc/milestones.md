# Milestones

## 1. Alert Explainer
- Single webhook endpoint for one monitoring service
- Hardcoded adaptor to parse the speicific webhook format to Canonical Alert
- A single, stateless call to an LLM to generate a human-readable explanation.
- Notify a single destination (e.g., Slack).

## 2. Contextualizer
- Introduce a Vector Database and implement RAG, perform a semantic search for alert details.
  - Stores Runbooks, Playbooks, Post-mortems, Incident Reports, Service Catalogs, Metadata, Resolved Tickets,
  - Building Knowledge Base Connector to Vector Database

## 3. Junior Investigator
- Enable the LLM to actively fetch more to form a hypothesis.
- Build the Data Abstraction Layer, make LLM agent access to data tools.
- Develop the ReAct (Reason + Act) Loop to make LLM analyze the alert, forms a hypothesis, and decides which tool to gather evidence
- Introduce a simple database to track the investigation stateless

## 4. Universal Adaptor Platform
- Make the system univeral, production-ready
- Refactor adapters to ingestion and data-fetching logic for each tools into its own pluggable module.
- Implement Ingestion, Action adaptors
  - adaptors for monitoring tools
  - Ticket creation, incident trigger, message
-
