import pytest
from unittest.mock import MagicMock, patch
from src.services.vector_db_service import VectorDBService
from src.models.knowledge_base import KnowledgeBaseArticle

# Mock the chromadb library
@pytest.fixture
def mock_chromadb_client():
    """Mocks the chromadb.PersistentClient and its methods."""
    with patch('chromadb.PersistentClient') as mock_client_constructor:
        mock_client_instance = MagicMock()
        mock_collection = MagicMock()
        mock_client_instance.get_or_create_collection.return_value = mock_collection
        mock_client_constructor.return_value = mock_client_instance
        yield mock_client_instance, mock_collection

@pytest.fixture
def mock_embedding_function():
    """Mocks the SentenceTransformerEmbeddingFunction."""
    with patch('chromadb.utils.embedding_functions.SentenceTransformerEmbeddingFunction') as mock_ef:
        yield mock_ef

@pytest.fixture
def vector_db_service(mock_chromadb_client, mock_embedding_function):
    """Provides a VectorDBService instance with mocked dependencies."""
    db_path = "./test_db"
    collection_name = "test_collection"
    service = VectorDBService(db_path=db_path, collection_name=collection_name)
    return service

def test_initialization(mock_chromadb_client, mock_embedding_function):
    """Tests if the service initializes the client and collection correctly."""
    mock_client, mock_collection = mock_chromadb_client
    db_path = "./test_db"
    collection_name = "test_collection"

    service = VectorDBService(db_path=db_path, collection_name=collection_name)

    # Verify that the client was initialized with the correct path
    patch('chromadb.PersistentClient').assert_called_once_with(path=db_path)

    # Verify that the collection was retrieved with the correct name and embedding function
    mock_client.get_or_create_collection.assert_called_once()
    assert mock_client.get_or_create_collection.call_args[1]['name'] == collection_name
    assert service.collection == mock_collection


def test_add_documents_upserts_correctly(vector_db_service):
    """Tests that add_documents calls the upsert method with the correct data."""
    articles = [
        KnowledgeBaseArticle(
            id="1",
            source="Confluence",
            title="Test Article 1",
            content="This is the content of article 1.",
            url="http://example.com/1"
        ),
        KnowledgeBaseArticle(
            id="2",
            source="Confluence",
            title="Test Article 2",
            content="This is the content of article 2.",
            url="http://example.com/2"
        )
    ]

    vector_db_service.add_documents(articles)

    # Extract expected data for assertion
    expected_ids = ["1", "2"]
    expected_documents = ["This is the content of article 1.", "This is the content of article 2."]
    expected_metadatas = [
        article.model_dump(exclude={"id", "content"}) for article in articles
    ]

    # Verify that the collection's upsert method was called correctly
    vector_db_service.collection.upsert.assert_called_once_with(
        ids=expected_ids,
        documents=expected_documents,
        metadatas=expected_metadatas
    )

def test_add_documents_with_no_articles(vector_db_service):
    """Tests that add_documents handles an empty list of articles gracefully."""
    vector_db_service.add_documents([])
    vector_db_service.collection.upsert.assert_not_called()

def test_query_documents(vector_db_service):
    """Tests that query_documents calls the query method and returns results."""
    query_texts = ["find me something"]
    n_results = 3
    mock_results = {"documents": [["result1"]]}
    vector_db_service.collection.query.return_value = mock_results

    results = vector_db_service.query_documents(query_texts, n_results=n_results)

    vector_db_service.collection.query.assert_called_once_with(
        query_texts=query_texts,
        n_results=n_results
    )
    assert results == mock_results

@pytest.mark.parametrize("db_path, collection_name", [("", None), (None, "")])
def test_initialization_failure(db_path, collection_name):
    """Tests that initialization raises an exception if dependencies fail."""
    with patch('chromadb.PersistentClient', side_effect=Exception("Connection failed")):
        pytest.raises(Exception, match="Connection failed")
        VectorDBService(db_path=db_path, collection_name=collection_name)
