# To-Do List

## Pre-Milestone 2: Testing Infrastructure

### High Importance
- [x] **Develop Comprehensive Test Suite:** Create unit and integration tests for existing Milestone 1 components (webhook endpoint, adapters, LLM integration, notification) to ensure stability and provide a safety net for future development.

## Milestone 2: Contextualizer

### High Importance
- [x] **Research and Select Vector Database:** Evaluate and choose a suitable vector database technology (e.g., Pinecone, Weaviate, FAISS, ChromaDB) based on project requirements and existing infrastructure.
  - ChromaDB will be used for initial development.
  - Additional VectorDB is considered for future.
- [x] **Integrate Vector Database:** Implement the necessary client code and configuration to connect to and interact with the selected vector database. (Likely in `src/services/` or a new `src/database/` module).
  - [x] **Setup ChromaDB for Vector Storage:** Add `chromadb` and `sentence-transformers` to the project dependencies in `pyproject.toml`.
  - [x] **Create `VectorDBService`:** Implement a service in `src/services/vector_db_service.py` to encapsulate all interactions with ChromaDB. It should handle client initialization, collection creation, document addition, and querying.
    - Implemented on `src/services/vector_db_service.py`
  - [x] **Update `AlertService`:** Modify `src/services/alert_service.py` to use the `VectorDBService` to search for relevant context based on the incoming alert's content. -> done
  - [x] **Update `get_explanation` in `llm.py`:** Enhance the prompt in `src/core/llm.py` by injecting the context retrieved from the vector database, providing the LLM with the necessary information to generate a more insightful explanation. -> done

- [x] **Implement RAG (Retrieval-Augmented Generation) Logic:** Develop the core logic to perform semantic searches in the vector database based on alert details and integrate the retrieved context into the LLM's prompt. (Likely in `src/core/llm.py` and `src/services/`).
  - Implemented with LangGraph

### Medium Importance
- **Develop Knowledge Base Connectors:** Create modules to ingest various types of knowledge (Runbooks, Playbooks, Post-mortems, Incident Reports, Service Catalogs, Metadata, Resolved Tickets) into the vector database. (Likely in `src/adapters/ingestion/` or a new `src/ingestion/` directory).
- **Define Knowledge Base Data Models:** Create Pydantic models (or similar) for the different knowledge document types to ensure consistent data structure for ingestion and retrieval. (Likely in `src/models/`).

### Low Importance
- **Initial Data Ingestion:** Populate the vector database with a small set of sample knowledge documents to facilitate initial testing and development of the RAG system.

## Milestone 3: Junior Investigator

### High Importance
- **Enable LLM to Fetch More Information:** Modify the LLM interaction to allow it to actively request and fetch additional data based on its current understanding and hypothesis. This will likely involve defining a set of "tools" or "functions" the LLM can call. (Likely in `src/core/llm.py` and `src/services/`).
- **Build Data Abstraction Layer:** Create a unified interface for the LLM agent to access various data sources (e.g., monitoring systems, ticketing systems, internal APIs). This layer will abstract away the complexities of different data formats and access methods. (Likely a new `src/data_abstraction/` module or within `src/services/`).
- **Develop ReAct (Reason + Act) Loop:** Implement the core logic for the LLM to analyze alerts, form hypotheses, decide which tools to use, execute tools, and refine its understanding. This will be an iterative process. (Likely in `src/services/` or a new `src/agent/` module).

### Medium Importance
- **Integrate Initial Data Tools:** Connect the Data Abstraction Layer to at least one external data source (e.g., a mock monitoring API, a simple internal database) that the LLM can query. (Likely in `src/adapters/` or `src/data_abstraction/`).
- **Design Investigation Tracking Database:** Define the schema for a simple database to track the state and progress of an investigation (e.g., current hypothesis, tools used, results). This database should be stateless from the LLM's perspective but provide persistence for the investigation. (Likely in `src/models/` and `src/database/` or `src/services/`).

### Low Importance
- **Implement Basic Investigation Tracking:** Develop the initial CRUD operations for the investigation tracking database. (Likely in `src/services/` and `src/database/`).
- **Logging and Monitoring for ReAct Loop:** Implement logging to observe the LLM's reasoning process and tool usage within the ReAct loop for debugging and analysis.

## Milestone 4: Universal Adaptor Platform

### High Importance
- **Refactor Adapters for Pluggability:** Redesign existing adapters and create a framework for easily adding new ingestion and action adapters. This should involve clear interfaces and a modular structure. (Likely in `src/adapters/` with new submodules for `ingestion` and `action`).
- **Implement Ingestion Adapters:** Develop concrete implementations for various monitoring tools (e.g., Prometheus, Grafana, Nagios) to convert their specific webhook formats into the Canonical Alert format. (Likely in `src/adapters/ingestion/`).
- **Implement Action Adapters:** Develop concrete implementations for actions like ticket creation (e.g., Jira, ServiceNow), incident triggering, and message sending (e.g., PagerDuty, Opsgenie, Microsoft Teams). (Likely in `src/adapters/notification/` or a new `src/adapters/action/`).

### Medium Importance
- **Develop Adapter Management System:** Create a mechanism (e.g., configuration files, database entries, or a simple UI) to manage and enable/disable different adapters dynamically. (Likely in `src/core/config.py` or a new `src/management/` module).
- **Error Handling and Robustness:** Implement comprehensive error handling, retry mechanisms, and logging for all adapter interactions to ensure system stability and reliability in a production environment.

### Low Importance
- **Documentation for New Adapters:** Provide clear documentation and examples for how to develop and integrate new ingestion and action adapters into the platform.
- **Performance Optimization:** Identify and address any performance bottlenecks in the adapter processing pipeline to ensure efficient handling of high volumes of webhooks and actions.
