import pytest
from unittest.mock import MagicMock, patch
from src.services.graph_service import GraphService
from src.models.canonical import CanonicalAlert

@pytest.fixture
def mock_vector_db_service():
    """Mocks the VectorDBService."""
    mock = MagicMock()
    mock.query_documents.return_value = {"documents": [["doc1", "doc2"]]}
    return mock

@pytest.fixture
def mock_llm():
    """Mocks the llm module functions."""
    with patch('src.services.graph_service.get_plan') as mock_get_plan, \
         patch('src.services.graph_service.generate_response') as mock_generate_response:
        mock_get_plan.return_value = [{"role": "assistant", "content": "Test plan"}]
        mock_generate_response.return_value = "Test response"
        yield mock_get_plan, mock_generate_response

@pytest.fixture
def graph_service(mock_vector_db_service):
    """Provides a GraphService instance with a mocked vector db service."""
    return GraphService(vector_db_service=mock_vector_db_service)

def test_run(graph_service, mock_vector_db_service, mock_llm):
    """Tests the run method of the GraphService."""
    mock_get_plan, mock_generate_response = mock_llm
    alert = CanonicalAlert(
        title="Test Alert",
        service="Test Service",
        severity="High",
        environment="Test Env",
        status="firing",
        timestamp="2025-07-10T10:00:00Z",
        details={},
        link_to_source="http://example.com",
        runbook_url="http://example.com",
        owner_team="",
        tags={},
        image_url="http://example.com",
        raw_payload={}
    )

    response = graph_service.run(alert)

    mock_get_plan.assert_called_once_with(alert)
    mock_vector_db_service.query_documents.assert_called_once()
    mock_generate_response.assert_called_once()

    assert response == "Test response"