from services.vector_db_service import VectorDBService
from core.config import DB_PATH, DB_COLLECTION_NAME

def search_knowledge_base(query: str) -> str:
    """Searches the knowledge base for a given query."""
    vector_db_service = VectorDBService(db_path=DB_PATH, collection_name=DB_COLLECTION_NAME)
    results = vector_db_service.query_documents(query_texts=[query], n_results=5)

    return results['documents'][0]
