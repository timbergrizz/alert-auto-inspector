import pytest
from unittest.mock import MagicMock, patch
from services.vector_db_service import VectorDBService

@pytest.fixture
def mock_chroma_client():
    with patch('chromadb.PersistentClient') as mock_client:
        yield mock_client

@pytest.fixture
def mock_embedding_function():
    with patch('chromadb.utils.embedding_functions.SentenceTransformerEmbeddingFunction') as mock_ef:
        yield mock_ef

@pytest.fixture
def vector_db_service(mock_chroma_client, mock_embedding_function):
    service = VectorDBService(path="./test_chroma_db")
    # Mock the collection object that would be returned by get_or_create_collection
    service.collection = MagicMock()
    return service

def test_get_or_create_collection(mock_chroma_client, vector_db_service):
    collection_name = "test_collection"
    mock_collection = MagicMock()
    mock_chroma_client.return_value.get_or_create_collection.return_value = mock_collection

    result_collection = vector_db_service.get_or_create_collection(collection_name)

    mock_chroma_client.return_value.get_or_create_collection.assert_called_once_with(
        name=collection_name,
        embedding_function=vector_db_service.embedding_function
    )
    assert result_collection == mock_collection
    assert vector_db_service.collection == mock_collection

def test_add_documents(vector_db_service):
    documents = ["doc1", "doc2"]
    metadatas = [{"source": "a"}, {"source": "b"}]
    ids = ["id1", "id2"]

    vector_db_service.add_documents(documents, metadatas, ids)

    vector_db_service.collection.add.assert_called_once_with(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

def test_add_documents_no_collection_initialized(mock_chroma_client, mock_embedding_function):
    service = VectorDBService(path="./test_chroma_db")
    with pytest.raises(ValueError, match="Collection not initialized. Call get_or_create_collection first."):
        service.add_documents(["doc"], [{"source": "a"}], ["id"])

def test_query_documents(vector_db_service):
    query_texts = ["query1"]
    n_results = 3
    mock_query_results = {"documents": [["result1", "result2"]]}
    vector_db_service.collection.query.return_value = mock_query_results

    results = vector_db_service.query_documents(query_texts, n_results)

    vector_db_service.collection.query.assert_called_once_with(
        query_texts=query_texts,
        n_results=n_results
    )
    assert results == mock_query_results

def test_query_documents_no_collection_initialized(mock_chroma_client, mock_embedding_function):
    service = VectorDBService(path="./test_chroma_db")
    with pytest.raises(ValueError, match="Collection not initialized. Call get_or_create_collection first."):
        service.query_documents(["query"])
